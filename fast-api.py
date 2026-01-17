import os
import requests
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
from pillow_heif import register_heif_opener

import requests

register_heif_opener()

app = FastAPI()

# Sightengine API
SIGHTENGINE_URL = "xxxx"
API_USER = "xxxxxx"
API_SECRET = "xxxxxx"

if not API_USER or not API_SECRET:
    raise RuntimeError("Sightengine API credentials not set")

@app.post("/detect-deepfake")
async def detect_deepfake(media: UploadFile = File(...)):
    """
    Accepts HEIF, HEIC, JPG, JPEG, PNG, WEBP, etc.
    Converts everything to JPEG and sends to Sightengine
    """

    if not media.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    try:
        # Read uploaded image
        image_bytes = await media.read()

        # Open with Pillow (HEIC/HEIF supported)
        image = Image.open(io.BytesIO(image_bytes))

        # Convert to RGB (JPEG does not support alpha)
        image = image.convert("RGB")

        # Save standardized JPEG in memory
        output_buffer = io.BytesIO()
        image.save(output_buffer, format="JPEG", quality=95, optimize=True)
        output_buffer.seek(0)

        files = {
            "media": (
                "image.jpg",          # unified filename
                output_buffer,
                "image/jpeg"
            )
        }

        data = {
            "models": "genai",
            "api_user": API_USER,
            "api_secret": API_SECRET,
        }

        response = requests.post(
            SIGHTENGINE_URL,
            files=files,
            data=data,
            timeout=60
        )

        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Sightengine request failed: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))