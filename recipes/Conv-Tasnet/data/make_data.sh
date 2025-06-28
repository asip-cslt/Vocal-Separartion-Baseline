#!/bin/bash

# data includes: /yourpath/RIRS_NOISES /yourpath/AISHELL-1 /yourpath/MUSIC
base_data_dir=/work106/wangth/data

data_lists_dir=data_lists

if [ ! -d "$data_lists_dir" ]; then
  echo "ERROR: Can't Find $data_lists_dir"
  exit 1
fi
find "$data_lists_dir" -type f -print0 \
  | xargs -0 sed -i "s|/work106/wangth/data|$base_data_dir|g"

echo "Change Base Path Done！"

# make train data
python make_data.py \
  --seed 42 \
  --speech_json_path "data_lists/AISHELL1_dev.json" \
  --music_json_path "data_lists/MUSIC21_dev.json" \
  --reverb_json_path "data_lists/reverb.json" \
  --save_path "baseline_train_data" \
  --save_csv "baseline_train_data.csv" \
  --num 30000

# make valid(test) data
python make_data.py \
  --seed 114514 \
  --speech_json_path "data_lists/AISHELL1_val.json" \
  --music_json_path "data_lists/MUSIC21_val.json" \
  --reverb_json_path "data_lists/reverb.json" \
  --save_path "baseline_valid_data" \
  --save_csv "baseline_valid_data.csv" \
  --num 300

