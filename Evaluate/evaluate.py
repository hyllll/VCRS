import fed
import json
import os
import random
import argparse
import numpy as np
from collections import defaultdict


def load_data(dataset):
    with open(f"../Dialogue/res/{dataset}/dialogue_info_{dataset}.json",'r') as load_f:
        coat = json.load(load_f)
    contexts = []
    for _, dialogue in coat.items():
        dialogue_content = dialogue["content"]
        context = []
        for _, text in dialogue_content.items():
            context.append(text)
        context = ' <|endoftext|> '.join(context)
        context = '<|endoftext|> ' + context + ' <|endoftext|>'
        contexts.append(context)
    
    return contexts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='dialogue evaluate')
    parser.add_argument('--dataset', 
                        type=str, 
                        default='coat', 
                        help='select dataset, option: coat, ml-1m, opendialKG, redial, inspire')
    parser.add_argument('--eval_num', 
                        type=int, 
                        default=400, 
                        help='the number of dialogues')
    args = parser.parse_args()
    data = load_data(args.dataset)
    model, tokenizer = fed.load_models("microsoft/DialoGPT-large")
    print("model load successful")

    scores = []
    data = random.sample(data, args.eval_num)
    for conversation in data:
        scores.append(fed.evaluate(conversation, model, tokenizer))

    fed_scores = defaultdict(list)
    for result in scores:
        score_val = 0.0
        for key, val in result.items():
            fed_scores[key].append(val)
            score_val += val 
        fed_scores['fed_overall'].append(score_val / len(result))

    save_dir = f'./res/{args.dataset}/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open(save_dir + f'{args.dataset}_results.json', 'w') as f:
        json.dump(fed_scores, f)
