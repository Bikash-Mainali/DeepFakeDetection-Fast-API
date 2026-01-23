import os
import requests
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image
import requests
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from fastapi.responses import JSONResponse
from fastapi import UploadFile, FastAPI, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import io
from pillow_heif import register_heif_opener

register_heif_opener()

app = FastAPI()

# Sightengine API
SIGHTENGINE_URL = "https://api.sightengine.com/1.0/check.json"
API_USER = "1217200205"
API_SECRET = "wTCmZ7k2ZR5YFxzzzYLZQJuyhuTfEJz8"

if not API_USER or not API_SECRET:
    raise RuntimeError("Sightengine API credentials not set")

class ImageRequest(BaseModel):
    image: str  # base64 string
    content_type: str  # e.g., "image/png", "image/jpeg"


# CORS settings
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, etc
    allow_headers=["*"],        # allow all headers
)
@app.post("/detect-deepfake")
async def detect_deepfake(request: ImageRequest):
    try:
        # 1️⃣ Decode base64 (already JPEG)
        image_bytes = base64.b64decode(request.image)

        # 2️⃣ Save to temp JPEG file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        # 3️⃣ Call Sightengine
        params = {
            "models": "genai",
            "api_user": API_USER,
            "api_secret": API_SECRET,
        }

        with open(tmp_path, "rb") as img_file:
            response = requests.post(
                SIGHTENGINE_URL,
                files={"media": img_file},
                data=params,
                timeout=30,
            )

        # 4️⃣ Cleanup
        os.remove(tmp_path)

        # 5️⃣ Return Sightengine response
        return response.json()

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process image: {str(e)}"
        )

@app.post("/detect-deepfake-test")
async def receive_image(request: ImageRequest):
    try:
        # Decode the base64 image
        image_bytes = base64.b64decode(request.image)
        img = Image.open(BytesIO(image_bytes))
        print(f"Received image of size: {img.size} and format: {img.format}")

        img = img.convert("RGB")  # Convert to RGB for JPEG

        print(f"Converted image to RGB, format: {img.format}")

        # Save as JPEG
        filename = "received_image.jpg"
        img.save(filename, format="JPEG")

        return {"status": "success", "saved_as": filename}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {e}")

