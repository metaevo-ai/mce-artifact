#!/bin/bash

uv run python -m mce.main \
    --workspace "workspace/finer" \
    --env "finer" \
    --train-data "env/finer/data/train.jsonl" \
    --val-data "env/finer/data/val.jsonl" \
    --model "deepseek/deepseek-chat-v3.1" \
    --iterations 5 \
    --start-iter 1 \
    --train-limit 200 \
    --val-limit 100 \
    --log-dir "logs/finer" \
    --train-batch-size 50
