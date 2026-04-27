# Unsloth
Unsloth server for finetuning. This is mainly for the DGX Spark and therefore assumes you are using CUDA.

## Start services

Run these commands from this directory:

```bash
cd /home/sridharn/docker-services/unsloth
```

### Unsloth Core

Unsloth Core starts a GPU-enabled JupyterLab environment with Unsloth and
finetuning dependencies installed. Use this service when you want to run
notebooks, training scripts, or experiments directly in the container.

Start Unsloth Core:

```bash
docker compose up -d --build unsloth
```

By default, JupyterLab listens on `http://localhost:8888`. The default token is
`unsloth`, so the login URL uses `?token=unsloth`.
Override the port or token if needed:

```bash
JUPYTER_PORT=8890 JUPYTER_TOKEN=your-token docker compose up -d --build unsloth
```

### Unsloth Studio

Unsloth Studio starts the Unsloth web UI. Use this service when you want the
browser-based Studio interface instead of working directly in JupyterLab.

> **DGX Spark note:** Unsloth Studio is currently unavailable on DGX Spark.
> Track the upstream issue here:
> [unslothai/unsloth#5101](https://github.com/unslothai/unsloth/issues/5101).

Start Unsloth Studio:

```bash
docker compose up -d --build unsloth-studio
```

By default, Unsloth Studio listens on `http://localhost:8889`.
Override the port if needed:

```bash
SERVER_PORT=8891 docker compose up -d --build unsloth-studio
```

Start both services:

```bash
docker compose up -d --build
```

Stop the services:

```bash
docker compose down
```
