# Introduction
This is the code for text-based conversation generation

## Installtion
install dependencies via:
```
cd ./Dialogue/
pip install -r requirements.txt
```

## Prepare Data
1. If you want to generate conversation in the moive domain, please download the [ml-1m.csv](https://drive.google.com/file/d/1iOum0fcgPzyvV5Mj8EuNdgtd0eLPz2qt/view?usp=sharing) and put it in `./data/ml-1m/`. The ml-1m.csv file contains the movie information scraped from the imdb website, and this file is divided into 10 columns: 

    ` | user_id | item_id | rating | timestamp | movie | director | actors | country | title | genres |`

2. Corresponding templates are in the `./config/` directory. You can also add some new templates to enrich the conversation.

## RUN
Generate conversation in the e-commerce domain.
```
python gen_coat.py
```
Generate conversation in the movie domain.
```
python gen_movie.py
```
You can find generated conversation in `./res/`, such as `dialogue_info_coat.json` or `dialogue_info_ml-1m.json`.