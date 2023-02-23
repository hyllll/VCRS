import IPython.display as ipd
import argparse
import os
import json
import random
import numpy as np
from pydub import AudioSegment
from utils import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dialogue')
    parser.add_argument('--dataset', 
                        type=str, 
                        default='coat', 
                        help='select dataset, option: coat, ml-1m')
    args = parser.parse_args()
    with open(f"./data/dialogue/dialogue_info_{args.dataset}.json",'r') as load_f:
        dialogue = json.load(load_f)
    vctk_to_speaker_id, total_speaker = preprocess_speaker_info()
    agent, user = load_vits_model()
    # text = "VITS is Awesome!"
    # audio = generate_agent_speech(agent, text)
    zero_audio = np.zeros((20000,), dtype=np.float32)
    zero_audio = ipd.Audio(zero_audio, rate=user[0].data.sampling_rate, normalize=False)
    with open(f'zero.wav', 'wb') as f:
        f.write(zero_audio.data)
    zero_wav = AudioSegment.from_wav("./zero.wav")
    thanks = ['thanks_Q', 'thanks_A']
    save_dir = f'./speech_res/{args.dataset}/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for k, v in dialogue.items():
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
        speaker_speed = round(random.uniform(0.9, 1.1), 3)  # only for user

        audio_list = []
        count = 0
        save_name = f'diaid{dia_id}_uid{user_id}_iid{item_id}_{age}_{gender}_{speaker}'
        for uttr_name, uttr in content.items():
            if (count % 2 == 0) and (uttr_name not in thanks):
                s_audio = generate_user_speech(user, uttr, speaker_id, speaker_speed)
            elif (count % 2 != 0) and (uttr_name not in thanks):
                s_audio = generate_agent_speech(agent, uttr)
            
            if uttr_name == 'thanks_Q':
                s_audio = generate_user_speech(user, uttr, speaker_id, speaker_speed)
            elif uttr_name == 'thanks_A':
                s_audio = generate_agent_speech(agent, uttr)
            count += 1
            with open(f'{uttr_name}.wav', 'wb') as f:
                f.write(s_audio.data)
            audio_list.append(uttr_name)
        tag = 0
        for i, uttr_name in enumerate(audio_list):
            wav_file = AudioSegment.from_wav(f"./{uttr_name}.wav")
            if tag == 0:
                combine_wav = wav_file
                combine_wav = combine_wav + zero_wav
                tag = 1
            else:
                combine_wav = combine_wav + wav_file
                if (i != (len(audio_list) - 1)) and (i != (len(audio_list) - 3)):
                    combine_wav = combine_wav + zero_wav
            os.remove(f"./{uttr_name}.wav")
        combine_wav.export(f"{save_dir}{save_name}.wav", format="wav")
        # break
        

        



