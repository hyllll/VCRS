import os
import sys
import numpy as np
import torch
import torchaudio
import argparse
import time
import tqdm as tqdm
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import Dataset,DataLoader
from transformers import Wav2Vec2Model, Wav2Vec2PreTrainedModel, AutoConfig
from sklearn.model_selection import train_test_split



class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

class AudioDataset(Dataset):
    def __init__(self, datalist, audio_path, target_sample_rate, transformation=None):
        self.datalist = datalist
        self.audio_path = audio_path
        self.target_sample_rate = target_sample_rate
        self.transformation = None
        if transformation:
            self.transformation = transformation
        
            
    def __len__(self):
        return len(self.datalist)
    
    def __getitem__(self,idx):
        audio_file_path = os.path.join(self.audio_path, self.datalist[idx])
        audio_name = self.datalist[idx]
        age_label, gender_label = self._get_label(audio_name)
        waveform, sample_rate = torchaudio.load(audio_file_path)
        if sample_rate != self.target_sample_rate:
            waveform = self._resample(waveform, sample_rate)
            
        return waveform, age_label, gender_label
        
    
    def _get_label(self, audio_name):
        name_list = audio_name.split('_')
        age_labels = {'under 20':0, '20-30':1, 'over 30':2}
        gender_labels = {'women':0, 'men':1}
        
        age = age_labels[name_list[-3]]
        gender = gender_labels[name_list[-2]]
        
        return age, gender
    
    def _resample(self, waveform, sample_rate):
        resampler = torchaudio.transforms.Resample(sample_rate,self.target_sample_rate)
        
        return resampler(waveform)


class Wav2Vec2ClassificationModel(Wav2Vec2PreTrainedModel):
    def __init__(self, config, hidden_size, dropout):
        super().__init__(config)
        
        self.wav2vec2 = Wav2Vec2Model(config)
        self.hidden_size = hidden_size
        self.fc = nn.Linear(config.hidden_size, self.hidden_size)
        self.dropout = nn.Dropout(dropout)
        self.gender_fc = nn.Linear(self.hidden_size, 2)
        self.age_fc = nn.Linear(self.hidden_size, 3)
        self.tanh = nn.Tanh()
        self.relu = nn.ReLU()
        
        self.init_weights()
        
    def freeze_feature_extractor(self):
        self.wav2vec2.feature_extractor._freeze_parameters()
    
    def merged_strategy(self, hidden_states):
        outputs = torch.mean(hidden_states, dim=1)
        
        return outputs
    
    def forward(
        self,
        input_values,
        attention_mask=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        labels=None,
    ):
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict
        with torch.no_grad():
            outputs = self.wav2vec2(
                input_values,
                attention_mask=attention_mask,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                return_dict=return_dict,
            )
        hidden_states = outputs[0]
        x = self.merged_strategy(hidden_states)
        x = self.fc(x)
        x = self.relu(x)
        x = self.dropout(x)
        gender_logits = self.gender_fc(x)
        gender_logits = F.log_softmax(gender_logits, dim=-1)
        age_logits = self.age_fc(x)
        age_logits = F.log_softmax(age_logits, dim=-1)
        
        return age_logits, gender_logits


def pad_sequence(batch):
    # Make all tensor in a batch the same length by padding with zeros
    batch = [item.t() for item in batch]
    batch = torch.nn.utils.rnn.pad_sequence(batch, batch_first=True, padding_value=0.)
    return batch.permute(0, 2, 1)

def collate_fn(batch):

    audios, age_labels, gender_labels = [], [], []

    for waveform, age, gender in batch:
        audios += [waveform]
        age_labels += [torch.tensor(age)]
        gender_labels += [torch.tensor(gender)]

    audios = pad_sequence(audios)
    age_labels = torch.stack(age_labels)
    gender_labels = torch.stack(gender_labels)

    return audios.squeeze(dim=1), age_labels, gender_labels

def train_single_epoch(model, dataloader, optimizer, device):
    model.train()
    losses = []
    for waveform, age_label, gender_label in tqdm.tqdm(dataloader):
        waveform = waveform.to(device)
        age_label = age_label.to(device)
        gender_label = gender_label.to(device)
        
        age_logits, gender_logits = model(waveform)
        
        age_loss = F.nll_loss(age_logits, age_label)
        gender_loss = F.nll_loss(gender_logits, gender_label)
        loss = age_loss + gender_loss
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    return losses

def get_likely_index(tensor):
    # find most likely label index for each element in the batch
    return tensor.argmax(dim=-1)

def number_of_correct(pred, target):
    # count number of correct predictions
    return pred.eq(target).sum().item()

def test_val_single_epoch(model, dataloader, device):
    model.eval()
    age_correct = 0
    gender_correct = 0
    for waveform, age_label, gender_label in tqdm.tqdm(dataloader):
        waveform = waveform.to(device)
        age_label = age_label.to(device)
        gender_label = gender_label.to(device)
        
        age_logits, gender_logits = model(waveform)  # batch * output
        
        age_pred = get_likely_index(age_logits) # batch
        gender_pred = get_likely_index(gender_logits)
        
        age_correct += number_of_correct(age_pred, age_label)
        gender_correct += number_of_correct(gender_pred, gender_label)
    
    age_accu = age_correct / len(dataloader.dataset) * 100.
    gender_accu = gender_correct / len(dataloader.dataset) * 100.
    
    return age_accu, gender_accu

def train(model, train_loader, val_loader, optimizer, device, epochs):
    for epoch in tqdm.tqdm(range(epochs)):
        losses = train_single_epoch(model, train_loader, optimizer, device)
        loss = np.mean(losses)
        age_accu, gender_accu = test_val_single_epoch(model, val_loader, device)
        writer.add_scalar('loss', loss, epoch+1)
        writer.add_scalar('age_accuracy', age_accu, epoch+1)
        writer.add_scalar('gender_accuracy', gender_accu, epoch+1)
        print(f"\nTrain Epoch: {epoch + 1} Loss: {loss:.6f} Age: {age_accu:.2f}% Gender: {gender_accu:.2f}%")
    print('Finished Training')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='speech classification')
    parser.add_argument('--batch_size', 
                        type=int, 
                        default=4,)
    parser.add_argument('--hidden_size', 
                        type=int, 
                        default=1024)
    parser.add_argument('--dropout', 
                        type=float, 
                        default=0.2)
    parser.add_argument('--epochs', 
                        type=int, 
                        default=20)
    parser.add_argument('--lr', 
                        type=float, 
                        default=0.0001)
    parser.add_argument('--test', 
                        type=int, 
                        default=1)
    parser.add_argument('--dataset', 
                        type=str, 
                        default='ml-1m')
    args = parser.parse_args()

    cur_time = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))[5:]

    save_tb_log_path = f'./tb_log/{cur_time}_{args.batch_size}'
    if not os.path.exists('./tb_log/'):
        os.makedirs('./tb_log/')
    writer = SummaryWriter(save_tb_log_path, flush_secs=30)

    save_log = f'./log/{cur_time}_{args.lr}_{args.dropout}_{args.batch_size}.log'
    sys.stdout = Logger(save_log, sys.stdout)
 
    seed = 2023
    np.random.seed(seed)
    torch.manual_seed(seed)

    input_dir = f'./data/{args.dataset}/'
    datalist = os.listdir(input_dir)
    
    ratio_train = 0.8
    ratio_val = 0.1
    ratio_test = 0.1

    remaining, test_set = train_test_split(datalist, test_size=ratio_test, random_state=2023)
    ratio_remaining = 1 - ratio_test
    ratio_val_adjusted = ratio_val / ratio_remaining
    train_set, val_set = train_test_split(remaining, test_size=ratio_val_adjusted, random_state=2023)


    if torch.cuda.is_available():
        device='cuda'
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.benchmark = False
    else:
        device='cpu'

    train_set = AudioDataset(train_set, input_dir, 16000)
    val_set = AudioDataset(val_set, input_dir, 16000)
    if args.test:
        test_set = AudioDataset(test_set, input_dir, 16000)

    if device == "cuda":
        num_workers = 1
        pin_memory = False
    else:
        num_workers = 0
        pin_memory = False

    train_loader = DataLoader(
        train_set,
        batch_size=args.batch_size,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    val_loader = DataLoader(
        val_set,
        batch_size=args.batch_size,
        shuffle=False,
        drop_last=False,
        collate_fn=collate_fn,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    if args.test:
        test_loader = DataLoader(
            test_set,
            batch_size=args.batch_size,
            shuffle=False,
            drop_last=False,
            collate_fn=collate_fn,
            num_workers=num_workers,
            pin_memory=pin_memory,
        )

    model_name_or_path = "lighteternal/wav2vec2-large-xlsr-53-greek"
    config = AutoConfig.from_pretrained(
        model_name_or_path,
        finetuning_task="wav2vec2_clf",
    )

    clf_model = Wav2Vec2ClassificationModel.from_pretrained(
        model_name_or_path,
        config=config,
        hidden_size=args.hidden_size,
        dropout=args.dropout,
    )

    clf_model = clf_model.to(device)

    optimizer = optim.Adam(clf_model.parameters(), lr=args.lr)
    clf_model.freeze_feature_extractor()

    train(clf_model, train_loader, val_loader, optimizer, device, args.epochs)

    if args.test:
        age_accu, gender_accu = test_val_single_epoch(clf_model, test_loader, device)
        torch.save(clf_model, f'./clf_model_{args.dataset}.pt')
        print(f"Test set: Age: {age_accu:.2f}% Gender: {gender_accu:.2f}%")

