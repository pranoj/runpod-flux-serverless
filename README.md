# FLUX.1-schnell on Runpod Serverless

Text-to-image API running on a Runpod serverless GPU. Send a prompt, get back an image.

Built this to learn how AI models get deployed to the cloud.

![Sample output](sample-output.png)

## Files

- `handler.py`: loads FLUX once and generates an image for each request
- `Dockerfile`: packages the handler and model weights
- `test_endpoint.py`: calls the endpoint and saves `output.png`

## Usage

```powershell
$env:RUNPOD_API_KEY = Read-Host "Runpod API key"
python test_endpoint.py "a cozy cabin in snowy mountains at sunset"
```

Request body:

```json
{"input": {"prompt": "a golden retriever astronaut on the moon", "seed": 42}}
```

The image comes back as base64. Same prompt + seed gives the same image.

## Notes

- Used schnell instead of dev: faster (4 steps) and Apache 2.0 licensed.
- Model weights are baked into the image, so the image is big (~35 GB).
- The Hugging Face token is passed as a build secret, so it's not stored in the image.
- Needs a 48 GB GPU.
- Cold starts on a new machine took 8–9 minutes. Runpod's model caching would fix that.