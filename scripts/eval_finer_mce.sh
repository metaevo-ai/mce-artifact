#!/bin/bash
# Evaluate finer environment using MCE context (large version)

uv run python -m mce.eval \
    --iter_dir "assets/context/finer/mce/context-l" \
    --env "finer" \
    --data "env/finer/data/test.jsonl" \
    --limit 500 \
    --model "deepseek/deepseek-chat-v3.1" \
    --save-results-to "results/finer_mce"
