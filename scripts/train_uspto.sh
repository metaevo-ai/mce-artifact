#!/bin/bash

uv run python -m mce.main \
    --workspace workspace/uspto \
    --env uspto \
    --train-data env/uspto/data/train.jsonl \
    --val-data env/uspto/data/val.jsonl \
    --model deepseek/deepseek-chat-v3.1 \
    --iterations 5 \
    --start-iter 1 \
    --train-limit 50 \
    --val-limit 50 \
    --log-dir logs/uspto \
    --train-batch-size 5