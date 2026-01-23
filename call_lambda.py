import requests
import base64

def detect_deepfake(image_path, lambda_url):
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    response = requests.post(
        lambda_url,
        json={
            'image': image_base64,
            'content_type': 'image/jpeg'
        }
    )

    return response.json()

# Usage

LAMBDA_URL = 'https://lvoflxezsaykumjfe42j3eje540ghjzw.lambda-url.us-west-2.on.aws'
LAMBDA_URL = 'http://localhost:8000/detect-deepfake-test'
result = detect_deepfake('tttttt.jpg', LAMBDA_URL)
print(result)