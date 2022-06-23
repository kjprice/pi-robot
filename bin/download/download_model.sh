#!/bin/bash

cd "$(dirname "$0")"

model_filename=resnet50_coco_best_v2.1.0.h5
model_filepath=.../models/$model_filename

# Taken from https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606
download_url=https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5/

if [ ! -f $model_filepath ]; then
  echo "Model $model_filepath not found, downloading now"
  curl -L $download_url > $model_filepath
else
  echo "Model $model_filepath already exists, nothing to do"
fi