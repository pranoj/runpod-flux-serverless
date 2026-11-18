FROM runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --ignore-installed cryptography && \
    pip install --no-cache-dir -r requirements.txt

ENV HF_HOME=/models

RUN --mount=type=secret,id=hf_token \
    HF_TOKEN=$(cat /run/secrets/hf_token) \
    python -c "from huggingface_hub import snapshot_download; \
    snapshot_download('black-forest-labs/FLUX.1-schnell', \
    ignore_patterns=['flux1-schnell.safetensors', 'ae.safetensors', '*.jpeg', 'images/*'])"

ENV HF_HUB_OFFLINE=1

COPY handler.py .

CMD ["python3", "-u", "handler.py"]