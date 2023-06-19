import os
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset,DataLoader
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
import tqdm as tqdm
import argparse
from transformers import Wav2Vec2Model, Wav2Vec2PreTrainedModel, AutoConfig


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
        x = self.dropout(x)
        x = self.fc(x)
        x = self.tanh(x)
        x = self.dropout(x)
        gender_logits = self.gender_fc(x)
        gender_logits = F.log_softmax(gender_logits, dim=-1)
        age_logits = self.age_fc(x)
        age_logits = F.log_softmax(age_logits, dim=-1)
        
        return age_logits, gender_logits

def construct_data(input_dir):
    datalist = os.listdir(input_dir)
    user = []
    item = []
    gender = []
    age = []
    name = []
    for file in datalist:
        u_id = int(file.split('_')[1][3:])
        i_id = int(file.split('_')[2][3:])
        user.append(u_id)
        item.append(i_id)
        
        name.append(file)
        gender.append(file.split('_')[-2])
        age.append(file.split('_')[-3])
    data = pd.DataFrame({'user':user, 'item':item, 'gender':gender, 'age':age, 'audio_name':name})

    return data

class GenDataset(Dataset):
    def __init__(self, df, audio_path):
        self.df = df
        self.audio_path = audio_path
        self.user = self.df.iloc[:,0].values
        self.item = self.df.iloc[:,1].values
        self.gender = self.df.iloc[:,2].values
        self.age = self.df.iloc[:,3].values
        self.audios = self.df.iloc[:,4].values
        self.age_labels = {'under 20':0, '20-30':1, 'over 30':2}
        self.gender_labels = {'women':0, 'men':1}

    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        user = self.user[index]
        item = self.item[index]
        gender = self.gender_labels[self.gender[index]]
        age = self.age_labels[self.age[index]]

        audio_file_path = os.path.join(self.audio_path, self.audios[index])
        waveform, sample_rate = torchaudio.load(audio_file_path)
        waveform = self._resample(waveform, sample_rate)

        return user, item, gender, age, waveform
    
    def _resample(self, waveform, sample_rate):
        resampler = torchaudio.transforms.Resample(sample_rate,16000)
        
        return resampler(waveform) 

def pad_sequence(batch):
    # Make all tensor in a batch the same length by padding with zeros
    batch = [item.t() for item in batch]
    batch = torch.nn.utils.rnn.pad_sequence(batch, batch_first=True, padding_value=0.)
    return batch.permute(0, 2, 1)

def collate_fn(batch):

    users, items, audios, age_labels, gender_labels = [], [], [], [], []

    for user, item, gender, age, waveform in batch:
        audios += [waveform]
        users += [torch.tensor(user)]
        items += [torch.tensor(item)]
        age_labels += [torch.tensor(age)]
        gender_labels += [torch.tensor(gender)]

    audios = pad_sequence(audios)
    users = torch.stack(users)
    items = torch.stack(items)
    age_labels = torch.stack(age_labels)
    gender_labels = torch.stack(gender_labels)

    return users, items, gender_labels, age_labels, audios.squeeze(dim=1)


def get_likely_index(tensor):
    # find most likely label index for each element in the batch
    return tensor.argmax(dim=-1)

def number_of_correct(pred, target):
    # count number of correct predictions
    return pred.eq(target).sum().item()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='generate label on audio')
    parser.add_argument('--model', 
                        type=str, 
                        default='ml-1m')
    parser.add_argument('--dataset', 
                        type=str, 
                        default='coat')
    args = parser.parse_args()

    model = torch.load(f'./clf_model_{args.model}.pt')
    audio_path = f'./data/{args.dataset}/'
    data = construct_data(audio_path)

    pre_data = GenDataset(data, audio_path)
    pre_loader = DataLoader(
        pre_data,
        batch_size=4,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=4,
        pin_memory=False,
    )

    model.eval()
    age_correct = 0
    gender_correct = 0
    tag = 1
    for user, item, gender_label, age_label, waveform in tqdm.tqdm(pre_loader):
        waveform = waveform.to("cuda")
        age_label = age_label.to("cuda")
        gender_label = gender_label.to("cuda")

        age_logits, gender_logits = model(waveform)

        age_pred = get_likely_index(age_logits) # batch
        gender_pred = get_likely_index(gender_logits)

        age_correct += number_of_correct(age_pred, age_label)
        gender_correct += number_of_correct(gender_pred, gender_label)

        if tag == 1:
            users = user.numpy()
            items = item.numpy()
            genders = gender_pred.cpu().numpy()
            ages = age_pred.cpu().numpy()
            tag = 0
        else:
            users = np.hstack((users, user.numpy()))
            items = np.hstack((items, item.numpy()))
            genders = np.hstack((genders, gender_pred.cpu().numpy()))
            ages = np.hstack((ages, age_pred.cpu().numpy()))

    
    age_accu = age_correct / len(pre_loader.dataset) * 100.
    gender_accu = gender_correct / len(pre_loader.dataset) * 100.
        
    print(f"Age: {age_accu:.2f}% Gender: {gender_accu:.2f}%")
    result_save_path = './res/'
    if not os.path.exists(result_save_path):
        os.makedirs(result_save_path)
    data = pd.DataFrame({'user':list(users), 'item':list(items), 'gender':list(genders), 'age':list(ages)})
    data.to_csv(f'./res/{args.dataset}_predict.csv', index=False)