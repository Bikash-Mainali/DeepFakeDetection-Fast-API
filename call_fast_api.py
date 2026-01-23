import requests
import base64
import json

def detect_deepfake(image_path, api_url):
    # Read image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Encode image to base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Prepare JSON payload
    payload = {
        "image": image_base64,
        "content_type": "image/png"  # change if your image is different
    }

    # Make POST request
    response = requests.post(api_url, json=payload)

    # Parse and return JSON
    try:
        return response.json()
    except json.JSONDecodeError:
        return {"error": "Invalid response from server", "status_code": response.status_code, "text": response.text}

# Call the API
API = 'http://localhost:8000/detect-deepfake'
#result = detect_deepfake('tttttt.jpg', API)
result = detect_deepfake('IMG_8224.HEIC', API)
print(json.dumps(result, indent=2))