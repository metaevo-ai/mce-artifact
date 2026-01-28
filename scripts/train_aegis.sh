#!/bin/bash
uv run python -m mce.main \
    --workspace "workspace/aegis2" \
    --env "aegis2" \
    --train-data "env/aegis2/data/train.jsonl" \
    --val-data "env/aegis2/data/val.jsonl" \
    --model "qwen/qwen3-8b" \
    --iterations 5 \
    --start-iter 1 \
    --train-limit 400 \
    --val-limit 400 \
    --log-dir "logs/aegis2" \
    --train-batch-size 50 \
    --evolve-retrieval