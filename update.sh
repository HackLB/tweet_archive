#!/usr/bin/env bash

dtstamp=$(date +%Y%m%d_%H%M%S)
. ~/.virtualenvs/tweet_archive/bin/activate

git pull
./archive.py
git add -A
git commit -m "$dtstamp"
git push

deactivate