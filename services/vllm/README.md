# vLLM Docker Compose

This folder runs the OpenAI-compatible vLLM server with Docker Compose.

## Requirements

- Docker with Compose support
- NVIDIA Container Toolkit
- A GPU visible to Docker

## Compose Files

Each supported model has its own compose file:

- `compose.qwen3-0.6b.yaml`: serves `Qwen/Qwen3-0.6B`
- `compose.qwen3.5-35b-a3b.yaml`: serves `Qwen/Qwen3.5-35B-A3B`

`compose.qwen3.5-35b-a3b.yaml` supports both HuggingFace download and fully offline operation
via a local model checkout (see [Offline Mode](#offline-mode) below).

## Environment

Create a local `.env` file in this directory:

```bash
cd /home/sridharn/docker-services/services/vllm
printf 'HF_TOKEN=hf_your_token_here\n' > .env
```

Variables read by the compose files:

- `HF_TOKEN`: passed into the container for HuggingFace downloads (not needed in offline mode).
- `HOME`: used by Compose to mount your host HuggingFace cache.
- `MODEL_DIR`: path to a locally cloned model repo (optional; see Offline Mode).

Do not commit `.env`. The repo root `.gitignore` already ignores `.env` files.

## Run

From this directory:

```bash
docker compose -f compose.qwen3-0.6b.yaml up
```

To run in the background:

```bash
docker compose -f compose.qwen3-0.6b.yaml up -d
```

To stop the server:

```bash
docker compose -f compose.qwen3-0.6b.yaml down
```

To run the larger model:

```bash
docker compose -f compose.qwen3.5-35b-a3b.yaml up
```

If you run Compose from the repo root instead, pass the compose file and env file explicitly:

```bash
docker compose --env-file services/vllm/.env -f services/vllm/compose.qwen3-0.6b.yaml up
```

## Offline Mode

`compose.qwen3.5-35b-a3b.yaml` can serve a model from a locally cloned HuggingFace repo with
no internet access. This is controlled by a custom `entrypoint.sh` wrapper that the compose file
mounts into the container.

**How the entrypoint decides which mode to use:**

- If `MODEL_DIR` is set in `.env` AND the directory it points to is non-empty once mounted at
  `/model`, the server starts in offline mode: `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`
  are set, and vllm is pointed at `/model` instead of the HuggingFace repo ID.
- Otherwise, vllm downloads the model from HuggingFace as normal.

**To run offline:**

1. Clone the model repo locally (requires `git-lfs`):

   ```bash
   git lfs install
   git clone https://huggingface.co/Qwen/Qwen3.5-35B-A3B /path/to/model
   ```

2. Add `MODEL_DIR` to `.env`:

   ```
   MODEL_DIR=/path/to/model
   ```

3. Start as usual:

   ```bash
   docker compose -f compose.qwen3.5-35b-a3b.yaml up
   ```

When `MODEL_DIR` is not set, the compose file falls back to a named Docker volume (`model_cache`)
for the `/model` mount, which is empty — this is what triggers the HuggingFace download path.

**Note on vllm's "offline inference" docs:** The vllm documentation uses "offline inference" to
mean *batch inference via the Python `LLM` class* (no HTTP server), as opposed to "online serving"
via `vllm serve`. This is a usage-pattern distinction, not a network one. Both modes can run
without internet access by pointing at a local model path, as this setup does.

## Test

List served models:

```bash
curl http://localhost:8000/v1/models
```

Run a small chat completion:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen3-0.6B","messages":[{"role":"user","content":"Say hello in one sentence."}],"max_tokens":32}'
```

Use `Qwen/Qwen3.5-35B-A3B` in the request body when running `compose.qwen3.5-35b-a3b.yaml`.
The model name is consistent regardless of whether you are in online or offline mode because
`--served-model-name Qwen/Qwen3.5-35B-A3B` is always passed to the server.

## Model Cache

When running in HuggingFace download mode, models are cached on the host at:

```
~/.cache/huggingface
```

The compose file mounts that cache into the container at `/root/.cache/huggingface`, so
downloaded weights persist across container restarts.

## Image

The compose files use the upstream vLLM OpenAI-compatible image directly:

```yaml
image: vllm/vllm-openai:latest
```
