#!/bin/bash
# Evaluate uspto environment using MCE context

uv run python -m mce.eval \
    --iter_dir "assets/context/uspto/mce" \
    --env "uspto" \
    --data "env/uspto/data/test.jsonl" \
    --limit 500 \
    --model "deepseek/deepseek-chat-v3.1" \
    --save-results-to "results/uspto_mce"
