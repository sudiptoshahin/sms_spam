## A binary text classification Spam/Ham

> Issue
Newer NLTK versions refuse to install into a directory that is writable by group/others, or owned by another user, because a swapped file could be installed as trusted data. Your ./env folder (the venv) has permissions like 775, so NLTK blocked the download and returned False.

__Solution__

```
ls -ld env
chmod go-w env

mkdir -p env/nltk_data
chmod 700 env/nltk_data
```

### Datasets

* __processed_v1.csv:__

>In this dataset i have remove all the stopwords

* __processed_v2.csv:__

>Without removing the stopwords

__Tasks__
-

1. __Project__
    * __Complete SMS_SPAM project complety front/back/ml__
    * __Customer Churn Prediction__
    * __CCTV Office employee monitoring__
2. __Docker__
3. __ML Ops__
    * Azure study topics with

4. __API Development__
    * __FasAPI__
5. __Video Lectures__
    0. __Transformer__
    1. __Hinton Deep Learning__
    2. __MIT Deep Learning__

6. __Complete 2 books__
    * Hands on ML
    * Deep learning
