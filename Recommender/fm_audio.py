import os
import argparse
import datetime
import torch
import pandas as pd
import numpy as np
import scipy.sparse as sp
import torch.utils.data as data
from tqdm import tqdm
from FMRecommender import PointFM
from utils import precision_at_k, recall_at_k, map_at_k, hr_at_k, ndcg_at_k, mrr_at_k
from utils import get_ur, get_feature, build_candidates_set, get_user_info


def age_map(age):
    if age < 20:
        return 0
    elif age >= 20 & age <= 30:
        return 1
    elif age > 30:
        return 2

def vote_user_info(df, u, mode):
    user_df = df[df['user'] == u]
    if mode == 0:
        gender_series = user_df['gender'].value_counts()
        gender = int(gender_series.idxmax())
        return gender
    elif mode == 1:
        age_series = user_df['age'].value_counts()
        age = int(age_series.idxmax())
        return age
    else:
        gender_series = user_df['gender'].value_counts()
        age_series = user_df['age'].value_counts()

        gender = int(gender_series.idxmax())
        age = int(age_series.idxmax())

        return gender, age

def load_data(path):
    df = pd.read_csv(path)
    df['user'] = pd.Categorical(df['user']).codes
    df['item'] = pd.Categorical(df['item']).codes
    user_num = df['user'].nunique()
    item_num = df['item'].nunique()
    print(user_num, item_num)
    return df, len(df), user_num, item_num

def split_testset(data, test_size=0.2):
    split_idx = int(np.ceil(len(data) * (1 - test_size)))
    train, test = data.iloc[:split_idx, :].copy(), data.iloc[split_idx:, :].copy()

    return train, test

class Sample(object):
    def __init__(self, user_num, item_num, feature_num, num_ng=4) -> None:
        self.user_num = user_num
        self.item_num = item_num
        self.num_ng = num_ng
        self.feature_num = feature_num
    
    def transform(self, data, is_training=True):
        if not is_training:
            neg_set = []
            for _, row in data.iterrows():
                u = int(row['user'])
                i = int(row['item'])
                r = row['rating']
                js = []
                if self.feature_num == 0:
                    g = int(row['gender'])
                    neg_set.append([u, i, g, r, js])
                elif self.feature_num == 1:
                    a = int(row['age'])
                    neg_set.append([u, i, a, r, js])
                elif self.feature_num == 2:
                    g = int(row['gender'])
                    a = int(row['age'])
                    neg_set.append([u, i, g, a, r, js])
                else:
                    neg_set.append([u, i, r, js])
            return neg_set
        
        user_num = self.user_num
        item_num = self.item_num
        pair_pos = sp.dok_matrix((user_num, item_num), dtype=np.float32)
        for _, row in data.iterrows():
            pair_pos[int(row['user']), int(row['item'])] = 1.0
        neg_set = []
        for _, row in data.iterrows():
            u = int(row['user'])
            i = int(row['item'])
            r = row['rating']
            js = []
            for _ in range(self.num_ng):
                j = np.random.randint(item_num)
                while (u, j) in pair_pos:
                    j = np.random.randint(item_num)
                js.append(j)
            if self.feature_num == 0:
                g = int(row['gender'])
                neg_set.append([u, i, g, r, js])
            elif self.feature_num == 1:
                a = int(row['age'])
                neg_set.append([u, i, a, r, js])
            elif self.feature_num == 2:
                g = int(row['gender'])
                a = int(row['age'])
                neg_set.append([u, i, g, a, r, js])
            else:
                neg_set.append([u, i, r, js])

        return neg_set
        

class FMData(data.Dataset):
    def __init__(self, neg_set, feature_num, is_training=True, neg_label_val=0.) -> None:
        super(FMData, self).__init__()
        self.features_fill = []
        self.labels_fill = []
        self.feature_num = feature_num
        self.neg_label = neg_label_val

        if self.feature_num == 0:
            self.init_gender(neg_set, is_training)
        elif self.feature_num == 1:
            self.init_age(neg_set, is_training)
        elif self.feature_num == 2:
            self.init_gender_age(neg_set, is_training)
        else:
            self.init_normal(neg_set, is_training)
    
    def __len__(self):
        return len(self.labels_fill)
    
    def __getitem__(self, index):
        features = self.features_fill
        labels = self.labels_fill
        user = features[index][0]
        item = features[index][1]
        label = labels[index]
        if self.feature_num == 0:
            gender = features[index][2]
            return user, item, gender, gender, label
        elif self.feature_num == 1:
            age = features[index][2]
            return user, item, age, age, label
        elif self.feature_num == 2:
            gender = features[index][2]
            age = features[index][3]
            return user, item, gender, age, label
        else:
            return user, item, item, item, label

    def init_gender(self, neg_set, is_training=True):
        for u, i, g, r, js in neg_set:
            self.features_fill.append([int(u), int(i), int(g)])
            self.labels_fill.append(r)

            if is_training:
                for j in js:
                    self.features_fill.append([int(u), int(j), int(g)])
                    self.labels_fill.append(self.neg_label)
        self.labels_fill = np.array(self.labels_fill, dtype=np.float32)
    
    def init_age(self, neg_set, is_training=True):
        for u, i, a, r, js in neg_set:
            self.features_fill.append([int(u), int(i), int(a)])
            self.labels_fill.append(r)

            if is_training:
                for j in js:
                    self.features_fill.append([int(u), int(j), int(a)])
                    self.labels_fill.append(self.neg_label)
        self.labels_fill = np.array(self.labels_fill, dtype=np.float32)
    
    def init_gender_age(self, neg_set, is_training=True):
        for u, i, g, a, r, js in neg_set:
            self.features_fill.append([int(u), int(i), int(g), int(a)])
            self.labels_fill.append(r)

            if is_training:
                for j in js:
                    self.features_fill.append([int(u), int(j), int(g), int(a)])
                    self.labels_fill.append(self.neg_label)
        self.labels_fill = np.array(self.labels_fill, dtype=np.float32)
    
    def init_normal(self, neg_set, is_training=True):
        for u, i, r, js in neg_set:
            self.features_fill.append([int(u), int(i)])
            self.labels_fill.append(r)

            if is_training:
                for j in js:
                    self.features_fill.append([int(u), int(j)])
                    self.labels_fill.append(self.neg_label)
        self.labels_fill = np.array(self.labels_fill, dtype=np.float32)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='fm recommender')
    parser.add_argument('--feature', 
                        type=str, 
                        default='user,item,rating')
    parser.add_argument('--val', 
                        type=int, 
                        default=0)
    parser.add_argument('--num_ng', 
                        type=int, 
                        default=5)
    parser.add_argument('--factors', 
                        type=int, 
                        default=32)
    parser.add_argument('--epochs', 
                        type=int, 
                        default=50)
    parser.add_argument('--lr', 
                        type=float, 
                        default=0.01)
    parser.add_argument('--batch_size', 
                        type=int, 
                        default=64)
    parser.add_argument('--dataset', 
                        type=str, 
                        default='ml-1m')
    args = parser.parse_args()
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    s_time = time[5:].replace(' ', '-').replace(':', '-')
    path = f'./res/{args.dataset}_predict.csv'
    df, record_num, user_num, item_num = load_data(path) 
    df.insert(df.shape[1], 'rating', 1)
    feature_list = args.feature.split(',')
    feature_num = get_feature(feature_list)
    df_data = df[feature_list]
    user_info = get_user_info(df_data, feature_num)
    train_set, test_set = split_testset(df_data,  0.2)
    if args.val:
        train_set, test_set = split_testset(train_set, 0.1)
    test_ur = get_ur(test_set)
    total_train_ur = get_ur(train_set)
    item_pool = set(range(item_num))
    sampler = Sample(user_num, item_num, feature_num, args.num_ng)
    neg_set = sampler.transform(train_set, is_training=True)
    print("data sample complete")
    train_dataset = FMData(neg_set, feature_num, is_training=True)
    model = PointFM(user_num, item_num, args.factors, args.epochs, args.lr, feature=feature_num)
    train_loader = data.DataLoader(
        train_dataset, 
        batch_size=args.batch_size, 
        shuffle=True, 
        num_workers=4
    )
    model.fit(train_loader)
    print('Start Calculating Metrics......')
    test_ucands = build_candidates_set(test_ur, total_train_ur, item_pool, 1000)
    print('')
    print('Generate recommend list...')
    print('')
    preds = {}
    for u in tqdm(test_ucands.keys()):
        if feature_num == 0:
            gender = vote_user_info(df_data, u, 0)
            tmp = pd.DataFrame({
                'user': [u for _ in test_ucands[u]], 
                'item': test_ucands[u], 
                'gender': [gender for _ in test_ucands[u]],
                'rating': [0. for _ in test_ucands[u]], # fake label, make nonsense
            })
        elif feature_num == 1:
            age = vote_user_info(df_data, u, 1)
            tmp = pd.DataFrame({
                'user': [u for _ in test_ucands[u]], 
                'item': test_ucands[u], 
                'age': [age for _ in test_ucands[u]],
                'rating': [0. for _ in test_ucands[u]], # fake label, make nonsense
            })
        elif feature_num == 2:
            gender, age = vote_user_info(df_data, u, 2)
            tmp = pd.DataFrame({
                'user': [u for _ in test_ucands[u]], 
                'item': test_ucands[u], 
                'gender': [gender for _ in test_ucands[u]],
                'age': [age for _ in test_ucands[u]],
                'rating': [0. for _ in test_ucands[u]], # fake label, make nonsense
            })
        else:
            tmp = pd.DataFrame({
                'user': [u for _ in test_ucands[u]], 
                'item': test_ucands[u], 
                'rating': [0. for _ in test_ucands[u]], # fake label, make nonsense
            })
        tmp_neg_set = sampler.transform(tmp, is_training=False)
        tmp_dataset = FMData(tmp_neg_set, feature_num, is_training=False)
        tmp_loader = data.DataLoader(
                tmp_dataset,
                batch_size=1000, 
                shuffle=False, 
                num_workers=4
            )
        for user, item, gender, age, label in tmp_loader:
            user = user.cuda()
            item = item.cuda()
            label = label.cuda()
            if feature_num == 0:
                gender = gender.cuda()
            elif feature_num == 1:
                age = age.cuda()
            elif feature_num == 2:
                gender = gender.cuda()
                age = age.cuda()

            if feature_num == 0:
                prediction = model.predict(user, item, g=gender)
            elif feature_num == 1:
                prediction = model.predict(user, item, a=age)
            elif feature_num == 2:
                prediction = model.predict(user, item, g=gender, a=age)
            else:
                prediction = model.predict(user, item)
            _, indices = torch.topk(prediction, 50)
            top_n = torch.take(torch.tensor(test_ucands[u]), indices).cpu().numpy()
        preds[u] = top_n
    
    for u in preds.keys():
        preds[u] = [1 if i in test_ur[u] else 0 for i in preds[u]]

    print('Save metric@k result to res folder...')
    if feature_num == 0:
        result_save_path = f'./res/fm_{args.dataset}_audio/gender/'
    elif feature_num == 1:
        result_save_path = f'./res/fm_{args.dataset}_audio/age/'
    elif feature_num == 2:
        result_save_path = f'./res/fm_{args.dataset}_audio/gender_age/'
    else:
        result_save_path = f'./res/fm_{args.dataset}_audio/no_ag/'
    if not os.path.exists(result_save_path):
        os.makedirs(result_save_path)
    res = pd.DataFrame({'metric@K': ['pre', 'rec', 'hr', 'map', 'mrr', 'ndcg']})
    for k in [1, 5, 10, 20, 30, 50]:
        tmp_preds = preds.copy()        
        tmp_preds = {key: rank_list[:k] for key, rank_list in tmp_preds.items()}

        pre_k = np.mean([precision_at_k(r, k) for r in tmp_preds.values()])
        rec_k = recall_at_k(tmp_preds, test_ur, k)
        hr_k = hr_at_k(tmp_preds, test_ur)
        map_k = map_at_k(tmp_preds.values())
        mrr_k = mrr_at_k(tmp_preds, k)
        ndcg_k = np.mean([ndcg_at_k(r, k) for r in tmp_preds.values()])

        if k == 10:
            print(f'Precision@{k}: {pre_k:.4f}')
            print(f'Recall@{k}: {rec_k:.4f}')
            print(f'HR@{k}: {hr_k:.4f}')
            print(f'MAP@{k}: {map_k:.4f}')
            print(f'MRR@{k}: {mrr_k:.4f}')
            print(f'NDCG@{k}: {ndcg_k:.4f}')

        res[k] = np.array([pre_k, rec_k, hr_k, map_k, mrr_k, ndcg_k])

    common_prefix = f'{args.num_ng}_{args.factors}_{args.lr}_{args.batch_size}_{args.val}'

    res.to_csv(
        f'{result_save_path}{common_prefix}_results.csv', 
        index=False
    )





