import pandas as pd
import numpy as np
import lightgbm as lgb
import random
import json
import os
from collections import defaultdict
from movie_utils import *
from config.movie_pattern import start_pattern, agent_pattern, user_pattern
from config.thanks_pattern import thanks_agent, thanks_user
from movie_attr import generate_country_dialogue, generate_genre_dialogue, generate_director_dialogue, generate_actor_dialogue


def load_data():
    movies = pd.read_csv("./data/ml-1m/ml-1m.csv")
    users = pd.read_csv("./data/ml-1m/users.dat", sep='::', names=['user_id', 'gender', 'age', 'occupation', 'zip'], engine='python')

    return (movies, users)

def get_user_item_info(data):
    movies = data[0]
    users = data[1]
    user_record = defaultdict(set)
    user_info = {}
    item_info = {}
    for _, row in movies.iterrows():
        user_id = int(row['user_id'])
        item_id = int(row['movie_id'])
        user_record[user_id].add(item_id)

        if user_id not in user_info.keys():
            user_info[user_id] = {}
            age = list(users[users['user_id'] == user_id]['age'])[0]
            gender = list(users[users['user_id'] == user_id]['gender'])[0]
            user_info[user_id]['age'] = get_user_age(age)
            user_info[user_id]['gender'] = get_user_gender(gender)
        
        if item_id not in item_info.keys():
            item_info[item_id] = {}
            item_info[item_id]['director'] = row['director']
            item_info[item_id]['country'] = modify_country(row['country'])
            item_info[item_id]['actor'] = get_item_actor(row['actors'])
            item_info[item_id]['genre'] = get_item_genre(row['genres'])
        
    
    return user_record, user_info, item_info

def calculate_user_preference(record, data):
    movies = data[0]
    columns = ["movie_id", "director", "actors", "country", "genres"]
    features_cols = ["director", "actors", "country", "genres"]
    user_preference = defaultdict(list)

    df_movie = movies[columns]
    df_movie = df_movie.drop_duplicates(keep='first')
    df_movie = df_movie.reset_index(drop=True)
    df_movie['director'] = pd.Categorical(df_movie['director']).codes
    df_movie['actors'] = pd.Categorical(df_movie['actors']).codes
    df_movie['country'] = pd.Categorical(df_movie['country']).codes
    df_movie['genres'] = pd.Categorical(df_movie['genres']).codes
    df_movie.insert(df_movie.shape[1], 'label', 0)

    for user in record:
        user_item_csv = df_movie.copy()
        record = list(user_record[user])
        for movie in record:
            user_item_csv.loc[user_item_csv['movie_id']==movie, 'label'] = 1
        X = user_item_csv[features_cols]
        Y = user_item_csv.label

        cls = lgb.LGBMClassifier(importance_type='gain')
        cls.fit(X, Y)

        indices = np.argsort(cls.booster_.feature_importance(importance_type='gain'))
        feature = [features_cols[i] for i in indices]

        user_preference[user] = feature
    
    return user_preference

def calculate_attr_weights(info, movie):
    genre_all = {}
    country_all = {}
    actor_all = {}
    director_all = {}

    for _, row in movie.iterrows():
        item_id = int(row['movie_id'])

        genres = info[item_id]['genre']
        for genre in genres:
            if genre not in genre_all.keys():
                genre_all[genre] = 1
            else:
                genre_all[genre] += 1
        
        country = info[item_id]['country']
        if country not in country_all.keys():
            country_all[country] = 1
        else:
            country_all[country] += 1
        
        director = info[item_id]['director']
        if director not in director_all.keys():
            director_all[director] = 1
        else:
            director_all[director] += 1
        
        actors = info[item_id]['actor']
        for actor in actors:
            if actor not in actor_all.keys():
                actor_all[actor] = 1
            else:
                actor_all[actor] += 1
    
    other_directors = [k for k,v in director_all.items() if v < 50] #402, 10415
    other_actors = [k for k,v in actor_all.items() if v < 50] #1267, 33893

    genre_weight = [genre_all[i] for i in sorted(genre_all)]
    country_weight = [country_all[i] for i in sorted(country_all)]
    director_weight = [director_all[i] for i in sorted(director_all)]
    actor_weight = [actor_all[i] for i in sorted(actor_all)]
    
    return (genre_weight, country_weight, director_weight, actor_weight), (genre_all, country_all, director_all, actor_all), (other_directors, other_actors)


if __name__ == '__main__':
    movie_data = load_data()
    user_record, user_info, item_info = get_user_item_info(movie_data)
    # user_preference = calculate_user_preference(user_record, movie_data)
    user_preference = np.load("./data/ml-1m/user_preference.npy", allow_pickle=True).item()
    weights, attr_counts, other_attr= calculate_attr_weights(item_info, movie_data[0])
    print("data load complete")
    dialogue_info = {}
    dialogue_id = 0
    for idx, row in movie_data[0].iterrows():
        user_id = int(row['user_id'])
        item_id = int(row['movie_id'])

        new_dialogue = {}
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
            english = True
            if slot == "country":
                country_val = item_info[item_id]["country"]
                utterance = generate_country_dialogue(agent_pattern, user_pattern, country_val)
            elif slot == "genres":
                genre_val = item_info[item_id]["genre"]
                utterance = generate_genre_dialogue(agent_pattern, user_pattern, genre_val, attr_counts[0], weights[0])
            elif slot == "director":
                director_val = item_info[item_id]["director"]
                utterance = generate_director_dialogue(agent_pattern, user_pattern, director_val, attr_counts[2], weights[2], other_attr[0])
                english = check_in_english(utterance)
                if not english:
                    break
            elif slot == "actors":
                actor_val = item_info[item_id]["actor"]
                utterance = generate_actor_dialogue(agent_pattern, user_pattern, actor_val, attr_counts[3], weights[3], other_attr[1])
                english = check_in_english(utterance)
                if not english:
                    break
            tmp_new_dialogue.append(utterance)
        if not english:
            continue
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
    
    res_path = './res/ml-1m/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    with open(res_path + 'dialogue_info.json', 'w') as f:
        json.dump(dialogue_info, f, indent=4)

