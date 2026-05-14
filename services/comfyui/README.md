# ComfyUI Docker Compose

This folder builds and runs ComfyUI with Docker Compose using an NVIDIA GPU.

## Requirements

- Docker with Compose support
- NVIDIA Container Toolkit
- A GPU visible to Docker

## Storage

Create the host folders before starting the service:

```bash
mkdir -p ~/.comfyui/{models,custom-nodes,output}
```

The compose file mounts these folders into the container:

- `~/.comfyui/models` -> `/opt/comfyui/models`
- `~/.comfyui/custom-nodes` -> `/opt/comfyui/custom_nodes`
- `~/.comfyui/output` -> `/opt/comfyui/output`

## Run

From this directory:

```bash
docker compose up --build -d
```

To stop the service:

```bash
docker compose down
```

To update ComfyUI, rebuild the image:

```bash
docker compose build --no-cache
docker compose up -d
```

## UI

Open ComfyUI at:

```text
http://localhost:8188
```

## Image

The Dockerfile builds from the official NVIDIA CUDA runtime image and clones the official ComfyUI repository:

```text
https://github.com/Comfy-Org/ComfyUI
```

By default it builds the `master` branch. To pin a specific branch, tag, or commit, set `COMFYUI_REF` as a build argument.
