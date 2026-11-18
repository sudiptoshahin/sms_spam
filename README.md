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

## Project structure

* __backend:__ `backend` directory is for the application backend. It is written in `FastAPI`. I've used `SQLite` database with `SQLAlchemy` ORM tool and `alembic` for database migration tool.
  * __alembic:__ Migration directory. `versions` is where the migration files are lived.
  * __app:__ `FastAPI` application directory
    * __artifacts:__ Directory is for the saved model which is used by the API.
    * __routers:__ Applications router directory.
    * __services:__ `service` is for the service layer where i've write the `inference/prediction` function that is used by the `/predict` API.
    * __database:__ `database` is for database connection/orm/session handling.
    * __models:__ decleare the ORM model.

* __frontend:__ `frontend` directory is for application frontend, Which is written in `React-ts-18.3.1`. And Call the backend api with js `fetch` library and store the data in react state and style the UI with `TailwindCSS`.

* __ml:__ `ml` directory is used for model RnD.
  * __artifacts:__ Save the trained model here
  * __config:__ config directory is for `Hyperparameters`
  * __notebooks:__ Notebook directory i've used for store the different versions of notebooks(`.ipynb`). Different version i used for different types of preprocessing and sequence preparation technique. `spam_detection_v2.ipynb` currently the main notebook. From this file i've preprocess and prepare the data and train the current model `TextSpamDetect_v2.1.onnx`.
  * __`requirements.txt`__ is only for the `MachineLearning` setup where we train and test the model according to our needs.

## Project setup

* __git clone <https://github.com/sudiptoshahin/sms_spam.git>__
* __cd sms_spam__

### Backend Setup

* __cd backend__

* __Create the environment:__
`python3 -m venv env` or `python -m venv env`

* __Activate the env:__
`source env/bin/activate`
* __Install dependencies:__  `pip install -r requirements.txt`
* __Fixing environment issue for `NLTK` data__

```
    ls -ld env
    chmod go-w env

    mkdir -p env/nltk_data
    chmod 700 env/nltk_data
```

* Then run `uvicorn app.main:app --reload`

> NB: First time it will take time to download the `nltk_data` in `backend/env/` directory. After a few minuites when the required downloads are completed then the server will starting and listening on port.
