#!/bin/bash

uv run python mce/main_online.py \
  --workspace workspace/aegis2_online \
  --env aegis2 \
  --test-data env/aegis2/data/test.jsonl \
  --test-limit 150 \
  --train-batch-size 10 \
  --data-accumulation-limit 30 \
  --model qwen/qwen3-8b \
  --log-dir logs/aegis2_online
