#!/bin/bash

uv run python mce/main_online.py \
  --workspace workspace/uspto_online \
  --env uspto \
  --test-data env/uspto/data/test.jsonl \
  --test-limit 100 \
  --train-batch-size 5 \
  --data-accumulation-limit 0 \
  --model deepseek/deepseek-chat-v3.1 \
  --log-dir logs/uspto_online