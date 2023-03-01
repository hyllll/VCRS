# Introduction
This is the code for the exploration of the two VCRSs datasets.

## Installtion
install dependencies via:
```
cd ./Recommender/
pip install -r requirements.txt
```

## Prepare Data
1. Download datasets from Google Drive: [coat.tar.gz](https://drive.google.com/file/d/1FnpYhMaeskckxGheKjar0U4YHIdDKM6K/view?usp=share_link) and [ml-1m.tar.gz](https://drive.google.com/file/d/1FnpYhMaeskckxGheKjar0U4YHIdDKM6K/view?usp=share_link)

2. Put the dataset in the `./data/` directory.

3. `tar -zxvf xxx.tar.gz`

## Multi-task Classification Module (MCM)
MCM aims to extract explicit semantic features (e.g., user age) from our created VCRS datasets.
* Extract features on Coat dataset
    ```
    python run_classifier.py --dataset='coat' --batch_size=64 --hidden_size=1024 --dropout=0.2 --epochs=20 --lr=0.0001 --test=1
    ```

* Extract features on ML-1M dataset
    ```
    python run_classifier.py --dataset='ml-1m' --batch_size=64 --hidden_size=1024 --dropout=0.2 --epochs=20 --lr=0.0001 --test=1
    ```

* The trained model is saved as `clf_model_xxx.pt`

## Voice Feature Integration Module (VFIM)
VFIM seeks to integrate the extracted voice-related features into the recommendation model for a performance-enhanced recommendation, which builds a two-phase fusion framework together with the MCM.
```
python run.py
```