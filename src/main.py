#!/usr/bin/env python3
"""Application for body measurement"""

import io
from typing import List

import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from PIL import Image

from model.model import BodyMeasurement

app = FastAPI()


@app.post("/measurement/")
async def get_measurements(data: UploadFile) -> List[float]:
    """Get body measurements from the input image.
    Args:
        data (UploadFile): The input image to estimate body measurements from.

    Raises:
        HTTPException: If the uploaded image is neither jpeg nor png.
        HTTPException: If the image could not be read.
        HTTPException: If the image has not exactly 3 channels.
        HTTPException: If the measurement could not be extracted.
    Returns:
        StreamingResponse: The response containing the image and keypoints.
    """
    if data.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, detail="Invalid mime type.")

    content = await data.read()
    if content is None:
        raise HTTPException(400, "Could not read file.")

    try:
        image = np.asarray(Image.open(io.BytesIO(content)))
        if image.ndim != 3:
            raise HTTPException(400, detail="Invalid image channels.")

        bm_ = BodyMeasurement()
        landmarks = bm_.get_world_landmarks(image)
        result = bm_.get_features(landmarks)

        return result
    except Exception as exc:
        raise HTTPException(400, "Could not determine pose.") from exc


if __name__ == "__main__":
    uvicorn.run("main:app")
