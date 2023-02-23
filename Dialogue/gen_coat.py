import pandas as pd
import numpy as np
import lightgbm as lgb
import random
import json
import os
from coat_utils import *
from collections import defaultdict
from config.coat_pattern import start_pattern, agent_pattern, user_pattern
from config.thanks_pattern import thanks_agent, thanks_user
from coat_attr import generate_gender_dialogue, generate_jacket_dialogue, generate_color_dialogue

def load_data():
    coat = pd.read_csv("./data/coat/coat_info.csv")
    coat['age'] = coat['age'].apply(lambda age: age_map(age))
    item_feature = np.genfromtxt('./data/coat/item_features.ascii', dtype=None)

    return (coat, item_feature)

def calculate_user_preference(data):
    coat = data[0]
    item_feature = data[1]
    user_record = defaultdict(set)
    item_matrix = np.zeros((300, 3))
    for _, row in coat.iterrows():
        user_id = int(row['user'])
        item_id = int(row['item'])
        user_record[user_id].add(item_id)
        gender, jacket, color = get_item_index(item_feature, item_id)
        item_matrix[item_id][0] = gender
        item_matrix[item_id][1] = jacket
        item_matrix[item_id][2] = color
    
    item_csv = pd.DataFrame(item_matrix)
    item_csv.insert(item_csv.shape[1], 'label', 0)
    item_csv.columns = ['gender','jacket', 'color', 'label']
    features_cols = ['gender', 'jacket', 'color']
    user_preference = defaultdict(list)
    for user in range(300):
        user_item_csv = item_csv.copy()
        record = list(user_record[user])
        for item in record:
            user_item_csv.loc[item, 'label'] = 1
        X = user_item_csv[features_cols]
        Y = user_item_csv.label

        cls = lgb.LGBMClassifier(importance_type='gain')
        cls.fit(X, Y)

        indices = np.argsort(cls.booster_.feature_importance(importance_type='gain'))
        feature = [features_cols[i] for i in indices]

        user_preference[user] = feature
    
    return  user_preference

def get_user_item_info(data):
    user_info = {}
    item_info = {}
    coat = data[0]
    item_feature = data[1]
    for _, row in coat.iterrows():
        user_id = int(row['user'])
        item_id = int(row['item'])
        user_info[user_id] = {}
        user_info[user_id]['age'] = get_user_age(row['age'])
        user_info[user_id]['gender'] = get_user_gender(row['gender'])

        if item_id not in item_info.keys():
            gender, jacket, color = get_item_index(item_feature, item_id)
            item_info[item_id] = {}
            item_info[item_id]['gender'] = get_item_gender(gender)
            item_info[item_id]['jacket'] = get_item_type(jacket)
            item_info[item_id]['color'] = get_item_color(color)
    
    return  user_info, item_info

def calculate_attr_weights(data):
    gender_all = {}
    jacket_all = {}
    color_all = {}
    coat = data[0]
    item_feature = data[1]
    for _, row in coat.iterrows():
        item_id = int(row['item'])
        gender, jacket, color = get_item_index(item_feature, item_id)
        if gender not in gender_all.keys():
            gender_all[gender] = 1
        else:
            gender_all[gender] += 1
        
        if jacket not in jacket_all.keys():
            jacket_all[jacket] = 1
        else:
            jacket_all[jacket] += 1
        
        if color not in color_all.keys():
            color_all[color] = 1
        else:
            color_all[color] += 1
    
    gender_weight = [gender_all[i] for i in sorted(gender_all)]
    jacket_weight = [jacket_all[i] for i in sorted(jacket_all)]
    color_weight = [color_all[i] for i in sorted(color_all)]

    return (gender_weight, jacket_weight, color_weight), (gender_all, jacket_all, color_all)


if __name__ == '__main__':
    coat_data = load_data()
    user_preference = calculate_user_preference(coat_data)
    user_info, item_info = get_user_item_info(coat_data)
    weights, attr_counts = calculate_attr_weights(coat_data)
    print("data load complete")
    dialogue_info = {}
    dialogue_id = 0
    for _, row in coat_data[0].iterrows():
        user_id = int(row['user'])
        item_id = int(row['item'])

        new_dialogue = {}
        new_dialogue["user_id"] = user_id
        new_dialogue["item_id"] = item_id

        new_dialogue["user_gender"] = user_info[user_id]["gender"]
        new_dialogue["user_age"] = user_info[user_id]["age"]
        new_dialogue["content"] = {}
        new_dialogue["content"]["start"] = random.choice(start_pattern)

        dialouge_order = user_preference[user_id]
        tmp_new_dialogue = []

        for slot in dialouge_order:
            if slot == "gender":
                gender_val = item_info[item_id]["gender"]
                utterance = generate_gender_dialogue(agent_pattern, user_pattern, gender_val, attr_counts[0], weights[0])
            elif slot == "jacket":
                jacket_val = item_info[item_id]["jacket"]
                utterance = generate_jacket_dialogue(agent_pattern, user_pattern, jacket_val, attr_counts[1], weights[1])
            elif slot == "color":
                color_val = item_info[item_id]["color"]
                utterance = generate_color_dialogue(agent_pattern, user_pattern, color_val, attr_counts[2], weights[2])
            tmp_new_dialogue.append(utterance)
        print("finish:", dialogue_id)
        start_index = 0
        end_index = 0
        step = 0
        name = ["Q1", "A1", "Q2", "A2", "Q3", "A3", "Q4", "A4", "Q5", "A5", "Q6", "A6", "Q7", "A7", "Q8", "A8", "Q9", "A9", "Q10", "A10"]
        for dia in tmp_new_dialogue:
            end_index = len(dia) + end_index
            tmp_name = name[start_index : end_index]
            tmp_dia = []
            for _, v in dia.items():
                tmp_dia.append(v)
            for i, val in enumerate(tmp_name):
                new_dialogue["content"][val] = tmp_dia[i]
            start_index = end_index
        new_dialogue["content"]["thanks_user"] = random.choice(thanks_user)
        new_dialogue["content"]["thanks_agent"] = random.choice(thanks_agent)
        dialogue_info[dialogue_id] = new_dialogue
        dialogue_id = dialogue_id + 1


    res_path = './res/coat/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    with open(res_path + 'dialogue_info.json', 'w') as f:
        json.dump(dialogue_info, f, indent=4)


            



