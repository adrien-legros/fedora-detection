from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from typing import List
from pydantic import BaseModel
import numpy as np
import cv2
from remote_infer_grpc import ort_v5
import os

import base64
import time

GRPC_HOST = os.getenv('GRPC_HOST', 'localhost')
GRPC_PORT = os.getenv('GRPC_PORT', '9000')
MODEL_NAME = os.getenv('MODEL_NAME', 'fedora_detection')
CONF_THRESHOLD = float(os.getenv('CONF_THRESHOLD', 0.2))
IOU_THRESHOLD = float(os.getenv('IOU_THRESHOLD', 0.5))
CLASSES_FILE = 'classes.yaml'

class Box(BaseModel):
    xMax: float
    xMin: float
    yMax: float
    yMin: float

class Detection(BaseModel):
    box: Box
    class_: str
    label: str
    score: float

    class Config:
        allow_population_by_field_name = True
        fields = {
            'class_': 'class'
        }

class Detections(BaseModel):
    detections: List[Detection]

class ImageData(BaseModel):
    image_base64: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    # Use FileResponse to return the contents of the HTML file
    return FileResponse("static/index.html", media_type="text/html")

@app.post("/predictions", response_model=Detections)
async def predictions(image_base64: ImageData):
    start_pred = time.time()
    img_b64 = image_base64.image_base64
    encoded_data = img_b64.split(',')[1]
    contents = base64.b64decode(encoded_data)
    nparr = np.frombuffer(contents, np.uint8)
    img_data = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    out = infer(img_data, CONF_THRESHOLD, IOU_THRESHOLD)
    classes = infer.class_name()
    raw_detections = out.tolist()
    result = Detections(detections=[])
    for raw_detection in raw_detections:
        # Boxes are returned in xMax,xMin,yMax,yMin coordinates on the 640x640 image
        box = Box(xMax=raw_detection[2]/640, xMin=raw_detection[0]/640, yMax=raw_detection[3]/640, yMin=raw_detection[1]/640)
        class_number = int(raw_detection[5])
        detection = Detection(box=box, 
            class_=classes[class_number], label=classes[class_number].capitalize(), score=raw_detection[4])
        print(detection)
        result.detections.append(detection)
    end_pred = time.time() - start_pred
    print(f"Function completed in {end_pred}ms")
    return result

if __name__ == "__main__":
    import uvicorn
    infer=ort_v5(GRPC_HOST, GRPC_PORT, MODEL_NAME, 640, CLASSES_FILE)
    uvicorn.run(app, host="0.0.0.0", port=8080)