#!/bin/bash
# Evaluate crime_prediction environment using MCE context (lawbench)

uv run python -m mce.eval \
    --iter_dir "assets/context/lawbench/mce" \
    --env "crime_prediction" \
    --data "env/crime_prediction/data/test.jsonl" \
    --limit 500 \
    --model "deepseek/deepseek-chat-v3.1" \
    --save-results-to "results/crime_prediction_mce"
