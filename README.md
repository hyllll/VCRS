# VCRSs：Voice-based Conversational Recommender Systems
This project aims to provide two voice-based conversational recommender systems datasets in the e-commerce and movie domains.

## Dataset Description
You can download datasets from GoogleDrive. The datasets consist of two parts: [coat.tar.gz](https://drive.google.com/file/d/1FnpYhMaeskckxGheKjar0U4YHIdDKM6K/view?usp=share_link) and [ml-1m.tar.gz](https://drive.google.com/file/d/1FnpYhMaeskckxGheKjar0U4YHIdDKM6K/view?usp=share_link)

### Dataset files
The data file is formatted as a mp3 file and the file name form is `diaidxx_uidxx_iidxx_xx_xx_xx.mp3`.

For example, for file `diaid21_uid249_iid35_20-30_men_251.mp3`, its meaning is as follows:
```
diaid21: corresponds to dialogue 21 in the text-based conversation dataset
uid249: user id is 249
iid35: item id is 35
20-30: user's age is between 20 and 30
men: user's gender is male
251: corresponds to speaker p251 in vctk dataset
```
Speaker information on the vctk dataset can be found [here](www.udialogue.org/download/cstr-vctk-corpus.html)

### Case study
Here we provide a demo of a data file (i.e., `diaid21_uid249_iid35_20-30_men_251.mp3`) that contains text and audio dialogue between the user and the agent. 

https://user-images.githubusercontent.com/38367896/221455311-06c8ef5b-b873-4aab-9fdc-3c274908bbee.mp4


Note that since we currently only explore the impact of speech on VCRS from the user's perspective, only the user's speech is included in the provided dataset. If you want complete dialogue audio, you can generate it through the code we provide.

## Data Construction
Our VCRSs dataset creation task includes four steps: (1) backbone dataset selection; (2)text-based conversation generation; (3) voice-based conversation generation; and (4) quality evaluation.

### Backbone dataset selection
We choose [Coat](www.cs.cornell.edu/~schnabts/mnar/) and [ML-1M](grouplens.org/datasets/movielens/1m/) as our backbone datasets. Using user-item interactions and item features to simulate a text-based conversation between users and agents for recommendation and using user features to assign proper speakers.

### Text-based conversation generation
Please refer to [here](https://github.com/hyllll/VCRS/tree/main/Dialogue) for how to generate the text-based conversation and the code is in `./Dialogue/` directory.

### Voice-based conversation generation
Please refer to [here](https://github.com/hyllll/VCRS/tree/main/Speech) for how to generate the voice-based conversation.
