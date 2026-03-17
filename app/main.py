from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image

from .services.inference import run_detection

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
GENERATED_DIR = STATIC_DIR / "generated"

app = FastAPI(title="Area Segura CV")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Area Segura CV",
        },
    )


@app.head("/")
async def health_root() -> dict[str, str]:
    return {"status": "ok"}


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

    if image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        return templates.TemplateResponse(
            "analyze.html",
            {
                "request": request,
                "title": "Analisar Imagem",
                "result": None,
                "error": "Formato invalido. Envie JPG, PNG ou WEBP.",
            },
            status_code=400,
        )

    file_bytes = await image.read()
    image_id = uuid4().hex
    extension = Path(image.filename).suffix.lower() or ".jpg"

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    original_path = GENERATED_DIR / f"{image_id}_original{extension}"
    original_path.write_bytes(file_bytes)

    pil_image = Image.open(original_path).convert("RGB")

    detection = run_detection(pil_image)

    annotated_path = GENERATED_DIR / f"{image_id}_detectado.jpg"
    detection["annotated_image"].save(annotated_path, format="JPEG", quality=92)

    result = {
        "filename": image.filename,
        "has_person": detection["has_person"],
        "person_count": detection["person_count"],
        "total_detections": detection["total_detections"],
        "restricted_risk": detection["restricted_risk"],
        "objects": detection["objects"],
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
