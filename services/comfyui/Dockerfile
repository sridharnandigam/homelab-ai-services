FROM nvidia/cuda:13.0.2-cudnn-runtime-ubuntu24.04

ARG COMFYUI_REF=master
ARG USER_ID=1000
ARG GROUP_ID=1000

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN if getent group "${GROUP_ID}" > /dev/null; then \
        GROUP_NAME="$(getent group "${GROUP_ID}" | cut -d: -f1)"; \
    else \
        GROUP_NAME=comfy; \
        groupadd --gid "${GROUP_ID}" "${GROUP_NAME}"; \
    fi \
    && if getent passwd "${USER_ID}" > /dev/null; then \
        USER_NAME="$(getent passwd "${USER_ID}" | cut -d: -f1)"; \
    else \
        USER_NAME=comfy; \
        useradd --uid "${USER_ID}" --gid "${GROUP_ID}" --create-home --shell /bin/bash "${USER_NAME}"; \
    fi \
    && mkdir -p "/home/${USER_NAME}" \
    && chown "${USER_ID}:${GROUP_ID}" "/home/${USER_NAME}" \
    && if [ "${USER_NAME}" != "comfy" ] && [ ! -e /home/comfy ]; then \
        ln -s "/home/${USER_NAME}" /home/comfy; \
    fi

WORKDIR /opt

RUN git clone --depth 1 --branch "${COMFYUI_REF}" https://github.com/Comfy-Org/ComfyUI.git comfyui

WORKDIR /opt/comfyui

RUN python3 -m venv /opt/comfyui/.venv \
    && /opt/comfyui/.venv/bin/pip install --upgrade pip setuptools wheel \
    && /opt/comfyui/.venv/bin/pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130 \
    && /opt/comfyui/.venv/bin/pip install -r requirements.txt \
    && mkdir -p models custom_nodes output \
    && chown -R "${USER_ID}:${GROUP_ID}" /opt/comfyui /home/comfy

ENV PATH="/opt/comfyui/.venv/bin:${PATH}"

USER ${USER_ID}:${GROUP_ID}

EXPOSE 8188

CMD ["python", "main.py", "--listen", "0.0.0.0", "--port", "8188"]
