#!/bin/bash

uv run python -m mce.main \
    --workspace "workspace/symptom_diagnosis" \
    --env "symptom_diagnosis" \
    --train-data "env/symptom_diagnosis/data/train.jsonl" \
    --val-data "env/symptom_diagnosis/data/val.jsonl" \
    --model "deepseek/deepseek-chat-v3.1" \
    --iterations 10 \
    --start-iter 1 \
    --train-limit 100 \
    --val-limit 100 \
    --log-dir "logs/symptom_diagnosis" \
    --train-batch-size 50 \
    --evolve-retrieval
