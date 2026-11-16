import base64
import io

import runpod
import torch
from diffusers import FluxPipeline

MODEL_ID = "black-forest-labs/FLUX.1-schnell"

pipe = FluxPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16)
pipe.to("cuda")

def handler(event):
    job_input = event["input"]

    prompt = job_input.get("prompt")
    if not prompt:
        return {"error": "Please provide a 'prompt' in the input."}

    width = job_input.get("width", 1024)
    height = job_input.get("height", 1024)
    steps = job_input.get("num_inference_steps", 4)
    seed = job_input.get("seed", 0)
    
    generator = torch.Generator("cpu").manual_seed(seed)

    image = pipe(
        prompt=prompt,
        width=width,
        height=height,
        num_inference_steps=steps,
        guidance_scale=0.0,
        max_sequence_length=256,
        generator=generator,
    ).images[0]

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {"image": image_base64, "prompt": prompt, "seed": seed}


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})