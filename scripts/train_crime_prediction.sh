#!/bin/bash

uv run python -m mce.main \
    --workspace "workspace/crime_prediction" \
    --env "crime_prediction" \
    --train-data "env/crime_prediction/data/train.jsonl" \
    --val-data "env/crime_prediction/data/val.jsonl" \
    --model "deepseek/deepseek-chat-v3.1" \
    --iterations 5 \
    --start-iter 1 \
    --train-limit 100 \
    --val-limit 100 \
    --log-dir "logs/crime_prediction" \
    --train-batch-size 50
    # --evolve-retrieval # Can be optionally enabled
