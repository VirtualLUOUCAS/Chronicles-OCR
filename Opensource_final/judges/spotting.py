"""字符检测（Detection / End-to-End Spotting）打分。

  - Detection：仅看 bbox，IoU > 0.75 视为 TP，包含 [UNK]
  - Spotting：IoU > 0.75 且字符匹配视为 TP，排除 [UNK]
均输出 per-sample F1。GT bbox 像素单位会被归一化到 0-1000 与模型输出对齐。
"""

from __future__ import annotations

from ..utils.unk import is_unk_char

IOU_THRESH = 0.75


def _iou(a, b) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    if ax2 <= ax1 or ay2 <= ay1 or bx2 <= bx1 or by2 <= by1:
        return 0.0
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = ix2 - ix1, iy2 - iy1
    if iw <= 0 or ih <= 0:
        return 0.0
    inter = iw * ih
    union = (ax2 - ax1) * (ay2 - ay1) + (bx2 - bx1) * (by2 - by1) - inter
    return inter / union if union > 0 else 0.0


def _parse_gt(row: dict) -> tuple[list[dict], int, int]:
    """解析 GT spotting，返回 [{'bbox':[x1,y1,x2,y2],'char':str}, ...] + 图像 W/H。"""
    sp = row.get("spotting") or []
    W = int(row.get("width") or 0)
    H = int(row.get("height") or 0)
    items: list[dict] = []
    for it in sp:
        if not isinstance(it, dict):
            continue
        ch = it.get("modern_char")
        if ch is None:
            ch = it.get("text", "")
        ch = str(ch or "").strip()

        bbox = it.get("bbox")
        if bbox is None:
            continue
        x1 = y1 = x2 = y2 = None
        if isinstance(bbox, dict):
            try:
                x1, y1, x2, y2 = (float(bbox[k]) for k in ("x1", "y1", "x2", "y2"))
            except (KeyError, TypeError, ValueError):
                continue
        elif isinstance(bbox, (list, tuple)) and len(bbox) == 4:
            try:
                bx = [float(v) for v in bbox]
            except (TypeError, ValueError):
                continue
            if bx[2] < bx[0] or bx[3] < bx[1]:
                x1, y1, x2, y2 = bx[0], bx[1], bx[0] + bx[2], bx[1] + bx[3]
            else:
                if "modern_char" in it:
                    x1, y1, x2, y2 = bx[0], bx[1], bx[0] + bx[2], bx[1] + bx[3]
                else:
                    x1, y1, x2, y2 = bx
        else:
            continue
        if x2 <= x1 or y2 <= y1:
            continue
        items.append({"bbox": [float(x1), float(y1), float(x2), float(y2)], "char": ch})
    return items, W, H


def _scale_to_1000(items: list[dict], W: int, H: int) -> list[dict]:
    if W <= 0 or H <= 0:
        return []
    sx, sy = 1000.0 / W, 1000.0 / H
    return [
        {"bbox": [it["bbox"][0] * sx, it["bbox"][1] * sy, it["bbox"][2] * sx, it["bbox"][3] * sy], "char": it["char"]}
        for it in items
    ]


def _match(preds: list[dict], gts: list[dict], iou_thresh: float, require_char: bool) -> tuple[int, int, int]:
    if not preds or not gts:
        return 0, len(preds), len(gts)
    pairs: list[tuple[float, int, int]] = []
    for pi, p in enumerate(preds):
        for gi, g in enumerate(gts):
            if require_char and p.get("char", "") != g.get("char", ""):
                continue
            iou = _iou(p["bbox"], g["bbox"])
            if iou >= iou_thresh:
                pairs.append((iou, pi, gi))
    pairs.sort(key=lambda x: x[0], reverse=True)
    used_p, used_g, tp = set(), set(), 0
    for _, pi, gi in pairs:
        if pi in used_p or gi in used_g:
            continue
        used_p.add(pi)
        used_g.add(gi)
        tp += 1
    return tp, len(preds) - tp, len(gts) - tp


def _f1(tp: int, fp: int, fn: int) -> float:
    if tp == 0:
        return 0.0
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    return 2 * p * r / (p + r) if (p + r) else 0.0


def judge(extract: dict, row: dict, iou_thresh: float = IOU_THRESH) -> dict:
    gt_raw, W, H = _parse_gt(row)
    gts = _scale_to_1000(gt_raw, W, H)

    preds_src = (extract or {}).get("items") or []
    preds: list[dict] = []
    for it in preds_src:
        if not isinstance(it, dict):
            continue
        bb = it.get("bbox")
        if not isinstance(bb, (list, tuple)) or len(bb) != 4:
            continue
        try:
            bb = [float(v) for v in bb]
        except (TypeError, ValueError):
            continue
        if bb[2] <= bb[0] or bb[3] <= bb[1]:
            continue
        preds.append({"bbox": bb, "char": str(it.get("char", "") or "").strip()})

    det_tp, det_fp, det_fn = _match(preds, gts, iou_thresh, require_char=False)
    det_f1 = _f1(det_tp, det_fp, det_fn)

    spot_gts = [it for it in gts if not is_unk_char(it["char"])]
    spot_preds = [it for it in preds if not is_unk_char(it["char"])]
    spot_tp, spot_fp, spot_fn = _match(spot_preds, spot_gts, iou_thresh, require_char=True)
    spot_f1 = _f1(spot_tp, spot_fp, spot_fn)

    return {
        "score": spot_f1,
        "iou_thresh": iou_thresh,
        "detection_f1": det_f1,
        "spotting_f1": spot_f1,
        "detection": {"tp": det_tp, "fp": det_fp, "fn": det_fn},
        "spotting": {"tp": spot_tp, "fp": spot_fp, "fn": spot_fn},
        "n_pred": len(preds),
        "n_gt": len(gts),
    }
