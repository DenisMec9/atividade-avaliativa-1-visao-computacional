from __future__ import annotations

from functools import lru_cache
import os
from typing import Any

from PIL import Image, ImageDraw
from transformers import pipeline

PERSON_THRESHOLD = 0.7
MODEL_NAME = os.getenv("HF_MODEL_ID", "hustvl/yolos-tiny")


@lru_cache(maxsize=1)
def get_detector():
    return pipeline(
        task="object-detection",
        model=MODEL_NAME,
        device=-1,
    )


def run_detection(image: Image.Image) -> dict[str, Any]:
    detector = get_detector()
    predictions = detector(image)

    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)

    objects = []
    person_count = 0

    for pred in predictions:
        label = pred["label"].lower()
        score = float(pred["score"])
        box = pred["box"]
        box_coords = [box["xmin"], box["ymin"], box["xmax"], box["ymax"]]

        is_person = label == "person" and score >= PERSON_THRESHOLD
        if is_person:
            person_count += 1

        color = "#e63946" if is_person else "#2a9d8f"
        draw.rectangle(box_coords, outline=color, width=3)
        draw.text(
            (box_coords[0] + 3, box_coords[1] + 3),
            f"{label} {score:.2f}",
            fill=color,
        )

        objects.append(
            {
                "label": label,
                "score": round(score, 3),
                "is_person": is_person,
            }
        )

    return {
        "annotated_image": annotated,
        "has_person": person_count > 0,
        "person_count": person_count,
        "restricted_risk": person_count > 0,
        "total_detections": len(predictions),
        "objects": sorted(objects, key=lambda item: item["score"], reverse=True),
        "threshold": PERSON_THRESHOLD,
        "model_name": MODEL_NAME,
    }
