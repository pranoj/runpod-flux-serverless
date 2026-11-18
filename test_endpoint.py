import base64
import json
import os
import sys
import time
import urllib.request

API_KEY = os.environ.get("RUNPOD_API_KEY")
ENDPOINT_ID = os.environ.get("RUNPOD_ENDPOINT_ID", "kth7z1pkrac4ll")
BASE_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}"


def call(path, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        BASE_URL + path,
        data=data,
        method="POST" if data else "GET",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "flux-test-client/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def main():
    if not API_KEY:
        sys.exit("Set RUNPOD_API_KEY first.")

    prompt = sys.argv[1] if len(
        sys.argv) > 1 else "a golden retriever astronaut on the moon"
    print(f"Sending prompt: {prompt}")
    start = time.time()

    result = call("/runsync", {"input": {"prompt": prompt, "seed": 42}})

    while result.get("status") in ("IN_QUEUE", "IN_PROGRESS"):
        print(f"Status: {result['status']}... waiting")
        time.sleep(5)
        result = call(f"/status/{result['id']}")

    if result.get("status") != "COMPLETED":
        sys.exit(f"Job did not complete: {result}")

    output = result["output"]
    if "error" in output:
        sys.exit(f"Handler error: {output['error']}")

    with open("output.png", "wb") as f:
        f.write(base64.b64decode(output["image"]))

    print(
        f"Saved output.png in {time.time() - start:.1f} seconds (seed {output['seed']})")


if __name__ == "__main__":
    main()
