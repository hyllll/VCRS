import torch
import vits_lib.commons as commons
import vits_lib.utils as vits_utils
from vits_lib.models import SynthesizerTrn
from vits_lib.text.symbols import symbols
from vits_lib.text import text_to_sequence
import IPython.display as ipd



def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

def get_vid_sid(line):
    '''
    Return:
        vctk_id: vctk id
        speaker_id: speaker id in vits
    '''
    line = line.split('|')
    vctk_id = int(line[0].split('/')[1][1:])
    speaker_id = int(line[1])

    return vctk_id, speaker_id

def split_speaker(s_info):
    # TODO: optimieze if else
    under_20_male = []
    under_20_female = []
    between_20_30_male = []
    between_20_30_female = []
    above_30_male = []
    above_30_female = []

    for i, info in enumerate(s_info):
        if i == 0:
            continue
        else:
            gender = info[10:11]
            age = int(info[6:8])
            user_id = int(info[1:4])
            if age < 20 and gender == 'M':
                under_20_male.append(user_id)
            elif age < 20 and gender == 'F':
                under_20_female.append(user_id)
            elif age >= 20 and age <=30 and gender == 'M':
                between_20_30_male.append(user_id)
            elif age >= 20 and age <=30 and gender == 'F':
                between_20_30_female.append(user_id)
            elif age > 30 and gender == 'M':
                above_30_male.append(user_id)
            else:
                above_30_female.append(user_id)

    between_20_30_female.remove(5)
    under_20_male.remove(315)

    total_speaker = []
    total_speaker.append(under_20_male)
    total_speaker.append(under_20_female)
    total_speaker.append(between_20_30_male)
    total_speaker.append(between_20_30_female)
    total_speaker.append(above_30_male)
    total_speaker.append(above_30_female)

    return total_speaker


def preprocess_speaker_info():
    with open('./data/speaker_info/speaker-info.txt') as f:
        lines = f.readlines()
    s_info = []
    for sub in lines:
        s_info.append(sub.replace("\n", ""))
    
    with open('./data/speaker_info/vctk_audio_sid_text_test_filelist.txt.cleaned.txt') as f:
        sid_text_test_filelist = f.readlines()
    with open('./data/speaker_info/vctk_audio_sid_text_train_filelist.txt.cleaned.txt') as f:
        sid_text_train_filelist = f.readlines()
    with open('./data/speaker_info/vctk_audio_sid_text_val_filelist.txt.cleaned.txt') as f:
        sid_text_val_filelist = f.readlines()
    filelist = sid_text_test_filelist + sid_text_train_filelist + sid_text_val_filelist
    vctk_to_speaker_id = {}
    for line in filelist:
        v_id, s_id = get_vid_sid(line)
        if v_id not in vctk_to_speaker_id.keys():
            vctk_to_speaker_id[v_id] = s_id
    total_speaker = split_speaker(s_info)

    return vctk_to_speaker_id, total_speaker


def load_vits_model():
    hps_agent = vits_utils.get_hparams_from_file("./vits_lib/configs/ljs_base.json")
    net_agent = SynthesizerTrn(
        len(symbols),
        hps_agent.data.filter_length // 2 + 1,
        hps_agent.train.segment_size // hps_agent.data.hop_length,
        **hps_agent.model).cuda()
    _ = net_agent.eval()
    _ = vits_utils.load_checkpoint("./vits_lib/pretrain/pretrained_ljs.pth", net_agent, None)

    hps_user = vits_utils.get_hparams_from_file("./vits_lib/configs/vctk_base.json")
    net_user = SynthesizerTrn(
        len(symbols),
        hps_user.data.filter_length // 2 + 1,
        hps_user.train.segment_size // hps_user.data.hop_length,
        n_speakers=hps_user.data.n_speakers,
        **hps_user.model).cuda()
    _ = net_user.eval()
    _ = vits_utils.load_checkpoint("./vits_lib/pretrain/pretrained_vctk.pth", net_user, None)

    return (hps_agent, net_agent), (hps_user, net_user)


def generate_agent_speech_audio(agent, text):
    hps_agent = agent[0]
    net_agent = agent[1]

    stn_tst = get_text(text, hps_agent)
    with torch.no_grad():
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        audio = net_agent.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1.0)[0][0,0].data.cpu().float().numpy()
    audio = ipd.Audio(audio, rate=hps_agent.data.sampling_rate, normalize=False)

    return audio


def generate_user_speech(user, text, sid, speaker_speed):
    hps_user = user[0]
    net_user = user[1]

    stn_tst = get_text(text, hps_user)
    with torch.no_grad():
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        sid = torch.LongTensor([sid]).cuda()
        audio = net_user.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=speaker_speed)[0][0,0].data.cpu().float().numpy()
    # audio = ipd.Audio(audio, rate=hps_user.data.sampling_rate, normalize=False)

    return audio


def generate_user_speech_audio(user, text, sid, speaker_speed):
    hps_user = user[0]
    net_user = user[1]

    stn_tst = get_text(text, hps_user)
    with torch.no_grad():
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        sid = torch.LongTensor([sid]).cuda()
        audio = net_user.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=speaker_speed)[0][0,0].data.cpu().float().numpy()
    audio = ipd.Audio(audio, rate=hps_user.data.sampling_rate, normalize=False)

    return audio



def selet_speaker_list_idx(age, gender):
    if age == 'under 20' and gender == 'men':
        return 0
    elif age == 'under 20' and gender == 'women':
        return 1
    elif age == '20-30' and gender == 'men':
        return 2
    elif age == '20-30' and gender == 'women':
        return 3
    elif age == 'over 30' and gender == 'men':
        return 4
    else:
        return 5