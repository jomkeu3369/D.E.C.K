import os
import sys
import base64
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from ultralytics import YOLO

from app.log import setup_logging, handle_exception
from app.model.crud import analyze_image_with_gpt

from dotenv import load_dotenv
load_dotenv()

model = YOLO('app/runs/segment/train/weights/best.pt')
router = APIRouter()

logger = setup_logging()
sys.excepthook = handle_exception

def cleanup_file(path: str):
    """백그라운드에서 임시 파일을 안전하게 삭제하는 함수"""
    try:
        os.remove(path)
    except OSError as e:
        print(f"Error removing file {path}: {e}")

@router.post("/analyze/llm", tags=["image"])
async def analyze_image_with_llm(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    analysis = await analyze_image_with_gpt(image_base64)
    return {"analysis": analysis}


@router.post("/analyze/yolo", tags=["image"])
async def analyze_image_with_yolo(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not model:
        return {"error": "Model is not loaded."}

    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_upload:
        tmp_upload.write(await file.read())
        upload_path = tmp_upload.name

    results = model.predict(upload_path)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_result:
        result_path = tmp_result.name

    if results:
        results[0].save(filename=result_path)
    else:
        cleanup_file(upload_path)
        return {"error": "Failed to get prediction results."}

    background_tasks.add_task(cleanup_file, upload_path)
    background_tasks.add_task(cleanup_file, result_path)

    return FileResponse(result_path)

        