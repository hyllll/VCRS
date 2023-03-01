import os
from turtle import forward
import numpy as np
import pandas as pd
import pickle
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn

class PointFM(nn.Module):
    def __init__(self, 
                 user_num, 
                 item_num, 
                 factors=84, 
                 epochs=20, 
                 lr=0.001,
                 reg_1 = 0.0,
                 reg_2 = 0.0001,
                 loss_type='CL',
                 optimizer='sgd',
                 gpuid='0', 
                 feature=0,
                 early_stop=True,
                 clf_model=None):
        super(PointFM, self).__init__()

        os.environ['CUDA_VISIBLE_DEVICES'] = gpuid
        # seed = 1
        # torch.cuda.manual_seed_all(seed)
        # torch.backends.cudnn.benchmark = False

        self.epochs = epochs
        self.lr = lr
        self.reg_1 = reg_1
        self.reg_2 = reg_2
        self.feature = feature
        self.embed_user = nn.Embedding(user_num, factors)
        self.embed_item = nn.Embedding(item_num, factors)

        self.u_bias = nn.Embedding(user_num, 1)
        self.i_bias = nn.Embedding(item_num, 1)
        if feature == 1:
            f = open('embedding_weight.pkl', 'rb') 
            embed_param = pickle.load(f)
            f.close()
            gender_weights = torch.FloatTensor(embed_param['gender_fc.weight'])
            gender_bias = torch.FloatTensor(embed_param['gender_fc.bias']).unsqueeze(dim=-1)
            self.embed_gender = nn.Embedding.from_pretrained(gender_weights, freeze=False) # （2, 1024）
            self.g_bias = nn.Embedding.from_pretrained(gender_bias, freeze=False)

            age_weights = torch.FloatTensor(embed_param['age_fc.weight'])
            age_bias = torch.FloatTensor(embed_param['age_fc.bias']).unsqueeze(dim=-1)
            self.embed_age = nn.Embedding.from_pretrained(age_weights, freeze=False)
            self.a_bias = nn.Embedding.from_pretrained(age_bias, freeze=False)
        elif feature == 2 or feature == 3:
            self.embed_gender = nn.Embedding(2, factors)
            self.g_bias = nn.Embedding(2, 1)
            self.embed_age = nn.Embedding(3, factors)
            self.a_bias = nn.Embedding(3, 1)

        self.bias_ = nn.Parameter(torch.tensor([0.0]))
        nn.init.normal_(self.embed_user.weight)
        nn.init.normal_(self.embed_item.weight)
        nn.init.constant_(self.u_bias.weight, 0.0)
        nn.init.constant_(self.i_bias.weight, 0.0)
        if feature == 2 or feature == 3:
            nn.init.normal_(self.embed_age.weight)
            nn.init.constant_(self.a_bias.weight, 0.0)
            nn.init.normal_(self.embed_gender.weight)
            nn.init.constant_(self.g_bias.weight, 0.0)
        
        if feature == 3:
            self.clf_model = torch.load('./clf_model.pt')

        self.loss_type = loss_type
        self.optimizer = optimizer
        self.early_stop = early_stop
    
    def forward(self, user, item, gender=None, age=None):
        embed_user = self.embed_user(user)
        embed_item = self.embed_item(item)

        pred = (embed_user * embed_item).sum(dim=-1, keepdim=True)
        pred += self.u_bias(user) + self.i_bias(item) + self.bias_

        if self.feature != 0:
            embed_gender = self.embed_gender(gender)
            embed_age = self.embed_age(age)
            pred += (embed_age * embed_user).sum(dim=-1, keepdim=True) + (embed_age * embed_item).sum(dim=-1, keepdim=True)
            pred += (embed_gender * embed_user).sum(dim=-1, keepdim=True) + (embed_gender * embed_item).sum(dim=-1, keepdim=True)
            pred += (embed_gender * embed_age).sum(dim=-1, keepdim=True)
            pred += self.a_bias(age) + self.g_bias(gender)
        
        return pred.view(-1)

    def clf_predict(self, waveform, model):
        age_logits, gender_logits = model(waveform)
        def get_likely_index(tensor):
            return tensor.argmax(dim=-1)
        age = get_likely_index(age_logits)
        gender = get_likely_index(gender_logits)

        return age, gender

    def fit(self, train_loader):
        if torch.cuda.is_available():
            self.cuda()
        else:
            self.cpu()
        
        optimizer = optim.SGD(self.parameters(), lr=self.lr)

        if self.loss_type == 'CL':
            criterion = nn.BCEWithLogitsLoss(reduction='sum')
        elif self.loss_type == 'SL':
            criterion = nn.MSELoss(reduction='sum')
        else:
            raise ValueError(f'Invalid loss type: {self.loss_type}')
        
        last_loss = 0.
        for epoch in range(1, self.epochs + 1):
            self.train()

            current_loss = 0.
            # set process bar display
            pbar = tqdm(train_loader)
            pbar.set_description(f'[Epoch {epoch:03d}]')
            for user, item, gender, age, label in pbar:
                user = user.cuda()
                item = item.cuda()
                label = label.cuda()
                if self.feature != 0 and self.feature != 3:
                    gender = gender.cuda()
                    age = age.cuda()
                    prediction = self.forward(user, item, gender=gender, age=age)
                elif self.feature == 3:
                    waveform = gender
                    self.clf_model.eval()
                    with torch.no_grad():
                        waveform = waveform.cuda()
                        age, gender = self.clf_predict(waveform, self.clf_model)
                    age = age.cuda()
                    gender = gender.cuda()
                    prediction = self.forward(user, item, gender=gender, age=age)
                else:
                    prediction = self.forward(user, item)
                loss = criterion(prediction, label)
                loss += self.reg_1 * (self.embed_item.weight.norm(p=1) + self.embed_user.weight.norm(p=1))
                loss += self.reg_2 * (self.embed_item.weight.norm() + self.embed_user.weight.norm())

                if self.feature != 0:
                    loss += self.reg_1 * (self.embed_gender.weight.norm(p=1) + self.embed_age.weight.norm(p=1))
                    loss += self.reg_2 * (self.embed_age.weight.norm() + self.embed_age.weight.norm())
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                pbar.set_postfix(loss=loss.item())
                current_loss += loss.item()
            
            self.eval()
            delta_loss = float(current_loss - last_loss)
            if (abs(delta_loss) < 1e-5) and self.early_stop:
                print('Satisfy early stop mechanism')
                break
            else:
                last_loss = current_loss
    
    def predict(self, u, i, g=None, a=None):
        if self.feature == 0:
            pred = self.forward(u, i).cpu()
        else:
            pred = self.forward(u, i, gender=g, age=a).cpu()
        
        return pred
