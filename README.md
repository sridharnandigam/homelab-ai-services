# docker-services

Deployment repo for local and cluster-hosted AI services.

This repo keeps service source and local Compose files separate from orchestrator
deployment manifests. The goal is to let the same images, ports, model paths,
and environment conventions work for local Docker Compose now, Docker Swarm on
DGX Spark nodes next, and Kubernetes later.

## Structure

```text
.
├── services/
│   ├── bifrost/
│   │   └── compose.yaml
│   ├── comfyui/
│   │   ├── compose.yaml
│   │   ├── Dockerfile
│   │   └── README.md
│   ├── llama-gemma/
│   │   └── compose.yaml
│   ├── llama-server/
│   │   ├── compose.yaml
│   │   ├── main.py
│   │   └── README.md
│   ├── openwebui/
│   │   └── compose.yaml
│   ├── portainer/
│   │   └── compose.yaml
│   ├── unsloth/
│   │   ├── compose.yaml
│   │   ├── Dockerfile.unsloth
│   │   ├── Dockerfile.unsloth-studio
│   │   └── README.md
│   └── vllm/
│       ├── compose.yaml
│       └── README.md
├── stacks/
│   └── swarm/
│       ├── llama-server.stack.yaml
│       ├── vllm.stack.yaml
│       └── README.md
├── k8s/
│   ├── base/
│   └── overlays/
│       ├── dgx-spark-ethernet/
│       └── dgx-spark-qsfp/
├── env/
│   ├── llama.env.example
│   ├── unsloth.env.example
│   └── vllm.env.example
└── llama/
    └── models/
```

## Services

Inference and training engines:

- **vllm** — upstream `vllm/vllm-openai` image, OpenAI-compatible endpoint on `:8000`. Host Hugging Face cache mounted from `~/.cache/huggingface`. Model selected via `MODEL` env var (defaults to `Qwen/Qwen3-0.6B`).
- **llama-server** — generic llama.cpp `server` for any GGUF under `${MODEL_DIR}`, exposed on `${LLAMA_PORT:-8080}`. Ships a `llama-cli` companion service for interactive runs.
- **llama-gemma** — llama.cpp server profile tailored for Gemma GGUFs, plus an optional `bench` profile that runs `llama-bench` and writes results to `./results`.
- **unsloth** — two services built from local Dockerfiles: `unsloth` (JupyterLab + Unsloth Core for fine-tuning on `:8888`) and `unsloth-studio` (browser UI on `:8889`, currently unsupported on DGX Spark — see service README).

Frontends and tooling:

- **openwebui** — chat UI on `:3000`, pre-pointed at a local vLLM at `host.docker.internal:8000` via the OpenAI-compatible API. Persists data in a named `open-webui-data` volume.
- **comfyui** — node-graph image generation UI on `:8188`. Built locally from the official ComfyUI repo; models, custom nodes, and outputs bind-mounted from `~/.comfyui/`.
- **portainer** — Portainer CE on `:9443` for container/stack management. Mounts the host Docker socket; state in the `portainer-data` named volume.
- **bifrost** — placeholder; compose file not yet populated.

## Local Compose

Run local development stacks from their service folders. Services that pull an
upstream image (vllm, llama-server, llama-gemma, openwebui, portainer) start
without a build step:

```bash
cd services/vllm
docker compose up -d
```

Services with a local Dockerfile (comfyui, unsloth) need `--build` on first run
or after image changes:

```bash
cd services/comfyui
docker compose up --build -d
```

Or from the repo root with an explicit file:

```bash
docker compose --env-file services/vllm/.env -f services/vllm/compose.yaml up -d
docker compose -f services/llama-gemma/compose.yaml up -d
docker compose -f services/llama-server/compose.yaml up -d
```

Local Compose files can keep developer conveniences like `build:`, bind mounts,
and `.env` files. Do not use them as the final Swarm or Kubernetes contract.

## Swarm

Swarm deployment files live in `stacks/swarm/`.

Before deploying to Swarm:

- Build images from `services/*` and push them to a registry reachable by every node.
- Create external Docker secrets such as `hf_token`.
- Make model and cache paths consistent on every node, for example `/mnt/models`
  and `/mnt/hf-cache`.
- Label GPU nodes, for example `docker node update --label-add gpu=true NODE`.

Deploy the current stacks:

```bash
docker stack deploy -c stacks/swarm/vllm.stack.yaml vllm
docker stack deploy -c stacks/swarm/llama-server.stack.yaml llama
```

See `stacks/swarm/README.md` for HF token handling and shared-storage
assumptions.

## Kubernetes

Kubernetes manifests belong under `k8s/`. Keep reusable service manifests in
`k8s/base/` and cluster-specific choices in `k8s/overlays/`.

The current overlays are placeholders for:

- `dgx-spark-ethernet`: current network setup.
- `dgx-spark-qsfp`: future high-speed fabric setup.

## Conventions

- Images should use registry-qualified names for cluster deployment.
- Secrets should be external to the repo.
- Model paths should converge on `/mnt/models`.
- Hugging Face cache paths should converge on `/mnt/hf-cache`.
- GPU nodes should be labeled consistently across orchestrators.
