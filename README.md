# docker-services

Small collection of Docker Compose based service folders.

## Structure

```text
.
├── bifrost/
│   └── compose.yaml
└── llama/
    ├── gemma/
    │   └── compose.yaml
    ├── nemotron/
    └── server/
        ├── compose.yaml
        └── main.py
```

## Directory Notes

- `bifrost/`: standalone service folder with its own `compose.yaml`.
- `llama/`: local area for `llama.cpp`-based services and model-specific stacks.
- `llama/gemma/`: model-specific Compose stack for Gemma.
- `llama/nemotron/`: reserved for a Nemotron-specific stack.
- `llama/server/`: generic `llama.cpp` server stack plus a small Python launcher.

## Compose Conventions

- Each service folder owns its own `compose.yaml`.
- Model-specific Compose stacks should use unique Compose project names to avoid collisions.
- Llama-related stacks currently mount models from `llama/models`.
- `llama/server/main.py` starts the `server` service in `llama/server/compose.yaml`.

## Typical Usage

Run a stack from the repo root with an explicit compose file:

```bash
docker compose -f llama/gemma/compose.yaml up -d
docker compose -f llama/server/compose.yaml up -d
```

## Why so many inference servers?
This is a dev setup and meant for experimentation with local AI. As such, it contains all the files for that. Not all of them need to be run for an end-to-end inference stack.