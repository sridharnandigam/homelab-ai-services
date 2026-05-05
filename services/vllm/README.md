# vLLM Docker Compose

This folder runs the OpenAI-compatible vLLM server with Docker Compose.

## Requirements

- Docker with Compose support
- NVIDIA Container Toolkit
- A GPU visible to Docker
- A Hugging Face token if the model requires authentication

## Environment

Create a local `.env` file in this directory:

```bash
cd /home/sridharn/docker-services/services/vllm
printf 'HF_TOKEN=hf_your_token_here\nMODEL=Qwen/Qwen3-0.6B\n' > .env
```

The compose file reads these variables:

- `HF_TOKEN`: passed into the container for Hugging Face downloads.
- `MODEL`: optional model name. Defaults to `Qwen/Qwen3-0.6B` if unset.
- `HOME`: used by Compose to mount your host Hugging Face cache.

Do not commit `.env`. The repo root `.gitignore` already ignores `.env` files.

To use a different model, edit `MODEL` in `.env`:

```bash
MODEL=mistralai/Mistral-7B-Instruct-v0.3
```

You can also override it for a single run:

```bash
MODEL=Qwen/Qwen3-4B docker compose up
```

## Run

From this directory:

```bash
docker compose up
```

To run in the background:

```bash
docker compose up -d
```

To stop the server:

```bash
docker compose down
```

If you run Compose from the repo root instead, pass the compose file and env file explicitly:

```bash
docker compose --env-file services/vllm/.env -f services/vllm/compose.yaml up
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

If you changed `MODEL`, use that model name in the request body.

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
