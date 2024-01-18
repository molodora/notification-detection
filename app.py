from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Body, HTTPException
from ultralytics import YOLO

from preprocessing import preprocess_image
from postprocessing import process_results
from utils import request_examples, response_examples, Image64, NotificationList


model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = Path(__file__).parent / "best.pt"
    global model
    model = YOLO(model_path)
    model.fuse()
    yield
    del model


app = FastAPI(
    title="NotificationDetection",
    description="The NotificationDetection App allows detecting window notifications on a mobile phone screenshot. \
        It is based on the YOLOv8 detection model.",
    version="0.0.1",
    contact={
        "name": "Malofeeva Alina",
        "url": "https://github.com/molodora",
    },
    lifespan=lifespan
)


@app.get("/", responses={200: {"content": {"application/json": {"example": {"health_check": "OK"}}}}})
async def root():
    return {"health_check": "OK"}


@app.get(
    "/model_info",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {"version": "0.1.0", "Number of layers": 295, "Number of parameters": 25859794}
                }
            }
        }
    },
    summary="General info about model",
    description="Returns model version, number of layers and parameters.",
    tags=["model"]
)
async def model_info():
    return {"version": "0.1.0", "Number of layers": model.info()[0], "Number of parameters": model.info()[1]}


@app.post(
    "/predict",
    response_model=NotificationList,
    responses=response_examples,
    summary="Detect notifications on screenshot",
    description="Uses yolov8 model to detect notification and button boxes. \
        Then it generates a response as required.",
    tags=["model"]
)
async def predict(
    image: Annotated[
        Image64,
        Body(openapi_examples=request_examples),
    ],
):
    try:
        pil_image = preprocess_image(image.screenshot)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not convert input string to image")
    
    results = model(source=pil_image)
    output = process_results(results)
    return output