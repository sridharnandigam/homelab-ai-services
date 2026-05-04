# Swarm Stacks

These files are deployment manifests for Docker Swarm. They are intentionally
separate from the local Compose files in `services/*`.

## Assumptions

- Images are pushed to a registry reachable by every Swarm node.
- GPU nodes are labeled with `gpu=true`.
- Model files are available at `/mnt/models` on each node or through shared storage.
- Hugging Face cache is available at `/mnt/hf-cache` on each node or through shared storage.
- Hugging Face authentication is provided either by `HF_TOKEN` at deploy time or
  by pre-populating `/mnt/hf-cache` with a `huggingface-cli login` token.

## Hugging Face Token

For a quick first deployment, export `HF_TOKEN` in the shell where you run
`docker stack deploy`:

```bash
export HF_TOKEN=hf_your_token_here
```

For longer-lived cluster use, prefer pre-populating `/mnt/hf-cache` on each node
or adding a small service-specific entrypoint wrapper that reads a Swarm secret
from `/run/secrets/hf_token` and exports `HF_TOKEN` before starting vLLM.

## Deploy

```bash
docker stack deploy -c stacks/swarm/vllm.stack.yaml vllm
docker stack deploy -c stacks/swarm/llama-server.stack.yaml llama
```

## Remove

```bash
docker stack rm vllm
docker stack rm llama
```
