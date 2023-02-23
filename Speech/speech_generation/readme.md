# Installtion
1. Install dependencies via:
    ```
    pip3 install -r requirements.txt
    ```
2. Build Monotonic Alignment Search
    ```
    cd ./vits_lib/monotonic_align
    python3 setup.py build_ext --inplace
    ```
# Pretrained model
1. Download [pretrained models](https://drive.google.com/drive/folders/1ksarh-cJf3F5eKJjLVWY0X1j1qsQqiS2) from google drive.

2. Put pretrained models in the ```pretrain``` folder
    ```
    mkdir ./vits_lib/pretrain/
    ```

# Run
1. Generate speech audio
    ```
    python3 inference.py --dataset='xxx'
    ```
    ```xxx``` is ```coat``` and ```ml-1m```
2. The results are saved in ```./speech_res/``` 

# Acknowledgement
Refer to the [vits repo](https://github.com/jaywalnut310/vits) to improve the code.