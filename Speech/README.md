# Introduction
This is the code for voice-based conversation generation

## Installtion
1. install dependencies via:
    ```
    cd ./Speech/
    pip install -r requirements.txt
    ```
2. Build Monotonic Alignment Search
    ```
    cd ./vits_lib/monotonic_align/
    python3 setup.py build_ext --inplace
    ```

## Pretrained model
1. Download [pretrained VITS models](https://drive.google.com/drive/folders/1ksarh-cJf3F5eKJjLVWY0X1j1qsQqiS2) from GoogleDrive. The pretrained models are provided by [VITS Repo](https://github.com/jaywalnut310/vits).

2. Put the pretrained models in the `./vits_lib/pretrain/` directory.

## RUN
1. Generate audio containing only the content of the user's conversation.
    ```
    python inference_user.py --dataset='xxx'
    ```
    ```xxx``` is ```coat``` or ```ml-1m```
2. Generate audio containing full conversations (i.e., users and agents).
    ```
    python inference.py --dataset='xxx'
    ```
    ```xxx``` is ```coat``` or ```ml-1m```
3. Note that all python scripts are used to generate complete audio on ml-1m, you can generate a certain number of audio according to your needs.
4. All results are saved in './speech_res/' directory.
