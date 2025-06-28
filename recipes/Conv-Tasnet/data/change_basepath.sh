#!/usr/bin/env bash

base_data_dir=$1

data_lists_dir=$2

if [ ! -d "$data_lists_dir" ]; then
  echo "ERROR: Can't Find $data_lists_dir"
  exit 1
fi
find "$data_lists_dir" -type f -print0 \
  | xargs -0 sed -i "s|/base_data_dir|$base_data_dir|g"

echo "Change Base Path Done！"
