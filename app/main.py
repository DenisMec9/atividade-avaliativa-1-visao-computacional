from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image, UnidentifiedImageError

from .services.inference import run_detection

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
GENERATED_DIR = STATIC_DIR / "generated"

app = FastAPI(title="Área Segura CV")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Área Segura CV",
        },
    )


@app.get("/analisar", response_class=HTMLResponse)
async def analyze_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "analyze.html",
        {
            "request": request,
            "title": "Analisar Imagem",
            "result": None,
            "error": None,
        },
    )


@app.post("/analisar", response_class=HTMLResponse)
async def analyze_image(request: Request, image: UploadFile = File(...)) -> HTMLResponse:
    if not image.filename:
        return templates.TemplateResponse(
            "analyze.html",
            {
                "request": request,
                "title": "Analisar Imagem",
                "result": None,
                "error": "Selecione uma imagem para continuar.",
            },
            status_code=400,
        )

    if image.content_type not in ALLOWED_CONTENT_TYPES:
        return templates.TemplateResponse(
            "analyze.html",
            {
                "request": request,
                "title": "Analisar Imagem",
                "result": None,
                "error": "Formato inválido. Envie JPG, PNG ou WEBP.",
            },
            status_code=400,
        )

    file_bytes = await image.read()
    image_id = uuid4().hex
    extension = ALLOWED_CONTENT_TYPES.get(image.content_type or "", ".jpg")

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    original_path = GENERATED_DIR / f"{image_id}_original{extension}"
    original_path.write_bytes(file_bytes)

    try:
        pil_image = Image.open(original_path).convert("RGB")
    except (UnidentifiedImageError, OSError):
        original_path.unlink(missing_ok=True)
        return templates.TemplateResponse(
            "analyze.html",
            {
                "request": request,
                "title": "Analisar Imagem",
                "result": None,
                "error": "Não foi possível ler a imagem enviada. Tente outro arquivo.",
            },
            status_code=400,
        )

    try:
        detection = run_detection(pil_image)
    except Exception:
        original_path.unlink(missing_ok=True)
        return templates.TemplateResponse(
            "analyze.html",
            {
                "request": request,
                "title": "Analisar Imagem",
                "result": None,
                "error": "Falha ao executar a inferência. Tente novamente em instantes.",
            },
            status_code=500,
        )

    annotated_path = GENERATED_DIR / f"{image_id}_detectado.jpg"
    detection["annotated_image"].save(annotated_path, format="JPEG", quality=92)

    result = {
        "filename": image.filename,
        "has_person": detection["has_person"],
        "person_count": detection["person_count"],
        "total_detections": detection["total_detections"],
        "restricted_risk": detection["restricted_risk"],
        "objects": detection["objects"],
        "object_counts": detection["object_counts"],
        "threshold": detection["threshold"],
        "original_url": f"/static/generated/{original_path.name}",
        "annotated_url": f"/static/generated/{annotated_path.name}",
    }

    return templates.TemplateResponse(
        "analyze.html",
        {
            "request": request,
            "title": "Analisar Imagem",
            "result": result,
            "error": None,
        },
    )


@app.get("/sobre", response_class=HTMLResponse)
async def about(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "title": "Sobre o Caso de Uso",
        },
    )
