#!/bin/bash
# Evaluate symptom_diagnosis environment using MCE context

uv run python -m mce.eval \
    --iter_dir "assets/context/symptom2disease/mce" \
    --env "symptom_diagnosis" \
    --data "env/symptom_diagnosis/data/test.jsonl" \
    --limit 500 \
    --model "deepseek/deepseek-chat-v3.1" \
    --save-results-to "results/symptom_diagnosis_mce"
