import argparse
import os
import subprocess
from pathlib import Path


DEFAULT_LLAMA_PORT = 30000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Start the llama.cpp docker compose service."
    )
    parser.add_argument(
        "gguf",
        help="Path to a GGUF file, for example ~/models/qwen2.5-7b-instruct.gguf.",
    )
    parser.add_argument(
        "--llama-port",
        type=int,
        default=DEFAULT_LLAMA_PORT,
        help=f"Host port for llama-server. Defaults to {DEFAULT_LLAMA_PORT}.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    compose_dir = Path(__file__).resolve().parent
    env = os.environ.copy()
    gguf_path = Path(os.path.expanduser(args.gguf)).resolve()

    env["MODEL_DIR"] = str(gguf_path.parent)
    env["LLAMA_MODEL"] = f"/models/{gguf_path.name}"
    env["LLAMA_PORT"] = str(args.llama_port)

    subprocess.run(
        ["docker", "compose", "up", "-d", "server"],
        cwd=compose_dir,
        env=env,
        check=True,
    )


if __name__ == "__main__":
    main()
