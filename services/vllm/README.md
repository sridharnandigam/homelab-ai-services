# vLLM Docker Compose

This folder runs the OpenAI-compatible vLLM server with Docker Compose.

## Requirements

- Docker with Compose support
- NVIDIA Container Toolkit
- A GPU visible to Docker
- A Hugging Face token if the model requires authentication

## Compose Files

Each supported model has its own compose file:

- `compose.qwen3-0.6b.yaml`: serves `Qwen/Qwen3-0.6B`
- `compose.qwen3.5-35b-a3b.yaml`: serves `Qwen/Qwen3.5-35B-A3B`

## Environment

Create a local `.env` file in this directory:

```bash
cd /home/sridharn/docker-services/services/vllm
printf 'HF_TOKEN=hf_your_token_here\n' > .env
```

The compose file reads these variables:

- `HF_TOKEN`: passed into the container for Hugging Face downloads.
- `HOME`: used by Compose to mount your host Hugging Face cache.

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

To run the larger model, use its compose file:

```bash
docker compose -f compose.qwen3.5-35b-a3b.yaml up
```

If you run Compose from the repo root instead, pass the compose file and env file explicitly:

```bash
docker compose --env-file services/vllm/.env -f services/vllm/compose.qwen3-0.6b.yaml up
```

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

## Model Cache

Models are cached on the host at:

```bash
~/.cache/huggingface
```

The compose file mounts that cache into the container at:

```bash
/root/.cache/huggingface
```

This keeps downloaded model files across container rebuilds and restarts.

## Image

The compose file uses the upstream vLLM OpenAI-compatible image directly:

```yaml
image: vllm/vllm-openai:latest
```
