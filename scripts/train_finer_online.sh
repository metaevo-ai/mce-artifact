#!/bin/bash

uv run python mce/main_online.py \
  --workspace workspace/finer_online \
  --env finer \
  --test-data env/finer/data/test.jsonl \
  --test-limit 100 \
  --train-batch-size 5 \
  --data-accumulation-limit 0 \
  --model deepseek/deepseek-chat-v3.1 \
  --log-dir logs/finer_online