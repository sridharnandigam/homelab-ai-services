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
│   ├── llama-gemma/
│   │   └── compose.yaml
│   ├── llama-server/
│   │   ├── compose.yaml
│   │   └── main.py
│   ├── unsloth/
│   │   ├── compose.yaml
│   │   ├── Dockerfile.unsloth
│   │   └── Dockerfile.unsloth-studio
│   └── vllm/
│       ├── compose.yaml
│       └── Dockerfile
├── stacks/
│   └── swarm/
│       └── *.stack.yaml
├── k8s/
│   ├── base/
│   └── overlays/
├── env/
│   └── *.env.example
└── llama/
    └── models/
```

## Local Compose

Run local development stacks from their service folders:

```bash
cd services/vllm
docker compose up --build
```

Or from the repo root with an explicit file:

```bash
docker compose --env-file services/vllm/.env -f services/vllm/compose.yaml up --build
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

Example:

```bash
docker stack deploy -c stacks/swarm/vllm.stack.yaml vllm
```

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
