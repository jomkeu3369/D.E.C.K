import sys
import base64
import tempfile
import subprocess

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from app.log import setup_logging, handle_exception
from app.model.crud import analyze_image_with_gpt

from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

logger = setup_logging()
sys.excepthook = handle_exception

@router.post("/analyze/llm", tags=["image"])
async def analyze_image_with_llm(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    analysis = await analyze_image_with_gpt(image_base64)
    return {"analysis": analysis}


@router.post("/analyze/yolo", tags=["image"])
async def analyze_image_with_yolo(file: UploadFile = File(...)):
    ...
    