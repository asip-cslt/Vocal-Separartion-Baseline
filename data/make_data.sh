#!/bin/bash

# You need to replace the file paths in the data lists with your data path.

# make train data
python data/make_data.py \
  --seed 42 \
  --speech_json_path "data/data_lists/AISHELL1_dev.json" \
  --music_json_path "data/data_lists/MUSIC21_dev.json" \
  --reverb_json_path "data/data_lists/reverb.json" \
  --save_path "data/baseline_train_data" \
  --save_csv "data/baseline_train_data.csv" \
  --num 60000

# make valid(test) data
python data/make_data.py \
  --seed 114514 \
  --speech_json_path "data/data_lists/AISHELL1_val.json" \
  --music_json_path "data/data_lists/MUSIC21_val.json" \
  --reverb_json_path "data/data_lists/reverb.json" \
  --save_path "data/baseline_valid_data" \
  --save_csv "data/baseline_valid_data.csv" \
  --num 10000

