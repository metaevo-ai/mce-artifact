#!/bin/bash
# Evaluate aegis2 environment using MCE context

uv run python -m mce.eval \
    --iter_dir "assets/context/aegis/mce" \
    --env "aegis2" \
    --data "env/aegis2/data/test.jsonl" \
    --limit 500 \
    --model "qwen/qwen3-8b" \
    --save-results-to "results/aegis2_mce"
