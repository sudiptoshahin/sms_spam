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