import IPython.display as ipd
import argparse
import os
import json
import random
import numpy as np
from tqdm import tqdm
from pydub import AudioSegment
from utils import *
import logging


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dialogue')
    parser.add_argument('--dataset', 
                        type=str, 
                        default='ml-1m', 
                        help='select dataset, option: coat, ml-1m')
    parser.add_argument('--format', 
                        type=str, 
                        default='mp3', 
                        help='select format, option: wav, flac, mp3')
    parser.add_argument('--start_id', 
                        type=int, 
                        default=0)
    args = parser.parse_args()
    with open(f"../Dialogue/res/{args.dataset}/dialogue_info_{args.dataset}.json",'r') as load_f:
        dialogue = json.load(load_f)
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    vctk_to_speaker_id, total_speaker = preprocess_speaker_info()
    agent, user = load_vits_model()
    random.seed(2023)
    save_dir = f'./speech_res/{args.dataset}_{args.format}_user/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for k, v in tqdm(dialogue.items()):
        dia_id = int(k)
        content = v['content']
        user_id = v['user_id']
        item_id = v['item_id']
        gender = v['user_gender']
        age = v['user_age']

        speaker_list_id = selet_speaker_list_idx(age, gender)
        speaker_list = total_speaker[speaker_list_id]
        speaker = random.choice(speaker_list)
        speaker_id = vctk_to_speaker_id[speaker]
        speaker_speed = 1.2

        audio_list = []
        count = 0
        save_name = f'diaid{dia_id}_uid{user_id}_iid{item_id}_{age}_{gender}_{speaker}'
        tag = 0
        for uttr_name, uttr in content.items():
            if count % 2 == 0:
                s_audio = generate_user_speech(user, uttr, speaker_id, speaker_speed)
                if tag == 0:
                    combine_audio = s_audio
                    tag = 1
                else:
                    combine_audio = np.hstack((combine_audio, s_audio))
            count += 1
        audio = ipd.Audio(combine_audio, rate=22050, normalize=False)
        with open(f'{save_dir}{save_name}.mp3', 'wb') as f:
            f.write(audio.data)
        

        



