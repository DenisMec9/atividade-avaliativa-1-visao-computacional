from __future__ import annotations

from functools import lru_cache
import os
from typing import Any

from PIL import Image, ImageDraw, ImageOps
from transformers import pipeline


def _get_person_threshold() -> float:
    env_value = os.getenv("PERSON_THRESHOLD", "0.7")
    try:
        parsed = float(env_value)
    except ValueError:
        return 0.7
    return max(0.0, min(parsed, 1.0))


def _get_detection_score_threshold() -> float:
    env_value = os.getenv("DETECTION_SCORE_THRESHOLD", "0.65")
    try:
        parsed = float(env_value)
    except ValueError:
        return 0.65
    return max(0.0, min(parsed, 1.0))


def _get_nms_iou_threshold() -> float:
    env_value = os.getenv("NMS_IOU_THRESHOLD", "0.45")
    try:
        parsed = float(env_value)
    except ValueError:
        return 0.45
    return max(0.0, min(parsed, 1.0))


def _get_min_box_area_ratio() -> float:
    env_value = os.getenv("MIN_BOX_AREA_RATIO", "0.001")
    try:
        parsed = float(env_value)
    except ValueError:
        return 0.001
    return max(0.0, min(parsed, 1.0))


def _get_enable_flip_tta() -> bool:
    env_value = os.getenv("ENABLE_FLIP_TTA", "true").strip().lower()
    return env_value in {"1", "true", "yes", "on"}


def _normalize_label(raw_label: str) -> str:
    label = raw_label.strip().lower()
    aliases = {
        "people": "person",
        "persons": "person",
        "human": "person",
    }
    return aliases.get(label, label)


def _sanitize_box(box: dict[str, Any], width: int, height: int) -> dict[str, float]:
    x_min = max(0.0, min(float(box["xmin"]), float(width)))
    y_min = max(0.0, min(float(box["ymin"]), float(height)))
    x_max = max(0.0, min(float(box["xmax"]), float(width)))
    y_max = max(0.0, min(float(box["ymax"]), float(height)))

    if x_max < x_min:
        x_min, x_max = x_max, x_min
    if y_max < y_min:
        y_min, y_max = y_max, y_min

    return {
        "xmin": x_min,
        "ymin": y_min,
        "xmax": x_max,
        "ymax": y_max,
    }


def _box_area_ratio(box: dict[str, float], width: int, height: int) -> float:
    box_area = max(0.0, box["xmax"] - box["xmin"]) * max(0.0, box["ymax"] - box["ymin"])
    image_area = max(1.0, float(width * height))
    return box_area / image_area


def _prepare_predictions(
    raw_predictions: list[dict[str, Any]],
    width: int,
    height: int,
) -> list[dict[str, Any]]:
    prepared: list[dict[str, Any]] = []
    for pred in raw_predictions:
        prepared.append(
            {
                "label": _normalize_label(str(pred["label"])),
                "score": float(pred["score"]),
                "box": _sanitize_box(pred["box"], width=width, height=height),
            }
        )
    return prepared


def _calculate_iou(box_a: list[float], box_b: list[float]) -> float:
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h

    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union_area = area_a + area_b - inter_area

    if union_area <= 0.0:
        return 0.0
    return inter_area / union_area


def _apply_classwise_nms(
    predictions: list[dict[str, Any]],
    iou_threshold: float,
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for pred in predictions:
        label = str(pred["label"]).lower()
        grouped.setdefault(label, []).append(pred)

    kept_predictions: list[dict[str, Any]] = []

    for _, label_predictions in grouped.items():
        remaining = sorted(label_predictions, key=lambda item: float(item["score"]), reverse=True)
        selected: list[dict[str, Any]] = []

        while remaining:
            best = remaining.pop(0)
            selected.append(best)

            best_box = best["box"]
            best_coords = [
                float(best_box["xmin"]),
                float(best_box["ymin"]),
                float(best_box["xmax"]),
                float(best_box["ymax"]),
            ]

            next_remaining: list[dict[str, Any]] = []
            for candidate in remaining:
                cand_box = candidate["box"]
                cand_coords = [
                    float(cand_box["xmin"]),
                    float(cand_box["ymin"]),
                    float(cand_box["xmax"]),
                    float(cand_box["ymax"]),
                ]
                iou = _calculate_iou(best_coords, cand_coords)
                if iou <= iou_threshold:
                    next_remaining.append(candidate)

            remaining = next_remaining

        kept_predictions.extend(selected)

    return kept_predictions


PERSON_THRESHOLD = _get_person_threshold()
DETECTION_SCORE_THRESHOLD = _get_detection_score_threshold()
NMS_IOU_THRESHOLD = _get_nms_iou_threshold()
MIN_BOX_AREA_RATIO = _get_min_box_area_ratio()
ENABLE_FLIP_TTA = _get_enable_flip_tta()
MODEL_NAME = os.getenv("HF_MODEL_ID", "hustvl/yolos-tiny")


@lru_cache(maxsize=1)
def get_detector():
    return pipeline(
        task="object-detection",
        model=MODEL_NAME,
        device=-1,
    )


def run_detection(image: Image.Image) -> dict[str, Any]:
    normalized_image = ImageOps.exif_transpose(image).convert("RGB")
    image_width, image_height = normalized_image.size

    detector = get_detector()
    raw_predictions = detector(normalized_image)

    predictions = _prepare_predictions(raw_predictions, width=image_width, height=image_height)

    if ENABLE_FLIP_TTA:
        mirrored_image = ImageOps.mirror(normalized_image)
        mirrored_raw = detector(mirrored_image)
        mirrored_prepared = _prepare_predictions(
            mirrored_raw,
            width=image_width,
            height=image_height,
        )

        for pred in mirrored_prepared:
            box = pred["box"]
            mirrored_x_min = float(box["xmin"])
            mirrored_x_max = float(box["xmax"])
            pred["box"] = {
                "xmin": max(0.0, float(image_width) - mirrored_x_max),
                "ymin": float(box["ymin"]),
                "xmax": min(float(image_width), float(image_width) - mirrored_x_min),
                "ymax": float(box["ymax"]),
            }

        predictions.extend(mirrored_prepared)

    filtered_predictions = [
        pred
        for pred in predictions
        if float(pred["score"]) >= DETECTION_SCORE_THRESHOLD
        and _box_area_ratio(pred["box"], width=image_width, height=image_height) >= MIN_BOX_AREA_RATIO
    ]
    predictions = _apply_classwise_nms(filtered_predictions, iou_threshold=NMS_IOU_THRESHOLD)

    annotated = normalized_image.copy()
    draw = ImageDraw.Draw(annotated)

    objects = []
    person_count = 0
    object_counts: dict[str, int] = {}

    for pred in predictions:
        label = pred["label"].lower()
        score = float(pred["score"])
        box = pred["box"]
        box_coords = [
            float(box["xmin"]),
            float(box["ymin"]),
            float(box["xmax"]),
            float(box["ymax"]),
        ]

        is_person = label == "person" and score >= PERSON_THRESHOLD
        if is_person:
            person_count += 1

        object_counts[label] = object_counts.get(label, 0) + 1

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
        "object_counts": dict(sorted(object_counts.items(), key=lambda item: item[1], reverse=True)),
        "threshold": PERSON_THRESHOLD,
        "score_threshold": DETECTION_SCORE_THRESHOLD,
        "nms_iou_threshold": NMS_IOU_THRESHOLD,
        "min_box_area_ratio": MIN_BOX_AREA_RATIO,
        "flip_tta_enabled": ENABLE_FLIP_TTA,
        "model_name": MODEL_NAME,
    }
