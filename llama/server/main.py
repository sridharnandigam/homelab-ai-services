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
        "model_name",
        help="Model filename in models directory, for example qwen2.5-7b-instruct.gguf.",
    )
    parser.add_argument(
        "--llama-port",
        type=int,
        default=DEFAULT_LLAMA_PORT,
        help=f"Host port for llama-server. Defaults to {DEFAULT_LLAMA_PORT}.",
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default="~/models/",
        help=f"Location of model ggufs"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    compose_dir = Path(__file__).resolve().parent
    env = os.environ.copy()

    env["MODEL_DIR"] = os.path.expanduser(args.model_dir)
    env["LLAMA_MODEL"] = f"/models/{args.model_name}"
    env["LLAMA_PORT"] = str(args.llama_port)

    subprocess.run(
        ["docker", "compose", "up", "-d", "server"],
        cwd=compose_dir,
        env=env,
        check=True,
    )


if __name__ == "__main__":
    main()
