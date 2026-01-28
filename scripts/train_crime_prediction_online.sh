#!/bin/bash

uv run python mce/main_online.py \
  --workspace workspace/crime_prediction_online \
  --env crime_prediction \
  --test-data env/crime_prediction/data/test.jsonl \
  --test-limit 100 \
  --train-batch-size 5 \
  --data-accumulation-limit 50 \
  --model deepseek/deepseek-chat-v3.1 \
  --log-dir logs/crime_prediction_online