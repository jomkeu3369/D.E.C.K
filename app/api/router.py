import sys
import base64
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from ultralytics import YOLO

from app.log import setup_logging, handle_exception
from app.model.crud import analyze_image_with_gpt

from dotenv import load_dotenv
load_dotenv()

model = YOLO('runs/segment/train/weights/best.pt')
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
    
    # 파일 임시 저장
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = Path(tmpdir) / file.filename
        with img_path.open("wb") as f:
            f.write(await file.read())

    output_dir = Path(tmpdir) / "results"
    results = model.predict(output_dir)

    for r in results:
        r.save(filename='result_seg.jpg')

    return FileResponse('result_seg.jpg')
        