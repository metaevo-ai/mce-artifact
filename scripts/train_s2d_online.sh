#!/bin/bash

uv run python mce/main_online.py \
  --workspace workspace/symptom_diagnosis_online \
  --env symptom_diagnosis \
  --test-data env/symptom_diagnosis/data/test.jsonl \
  --test-limit 212 \
  --train-batch-size 10 \
  --data-accumulation-limit 50 \
  --model deepseek/deepseek-chat-v3.1 \
  --log-dir logs/symptom_diagnosis_online