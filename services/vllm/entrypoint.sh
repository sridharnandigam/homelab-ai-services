#!/bin/bash
set -e

MODEL_PATH="/model/${HF_MODEL_ID}"

# If MODEL_DIR is set and the model subdirectory has content, run fully offline.
# Otherwise fall through to the default HuggingFace download path.
if [ -n "${MODEL_DIR}" ] && [ -d "${MODEL_PATH}" ] && [ "$(ls -A "${MODEL_PATH}" 2>/dev/null)" ]; then
    echo "[vllm] Local model detected at ${MODEL_PATH} — starting in offline mode"
    export HF_HUB_OFFLINE=1
    export TRANSFORMERS_OFFLINE=1
    exec python3 -m vllm.entrypoints.openai.api_server \
        --model "${MODEL_PATH}" \
        --served-model-name "${HF_MODEL_ID}" \
        "$@"
else
    echo "[vllm] MODEL_DIR not set or ${MODEL_PATH} is empty — downloading from HuggingFace"
    exec python3 -m vllm.entrypoints.openai.api_server \
        --model "${HF_MODEL_ID}" \
        "$@"
fi
