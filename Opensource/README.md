# Chronicles-OCR Benchmark

A multi-task benchmark for vision-language models on **Chinese historical script OCR**, covering all seven canonical scripts of Chinese characters: Oracle Bone (甲骨文), Bronze Script (金文), Seal Script (篆书), Clerical Script (隶书), Regular Script (楷书), Running Script (行书), Cursive Script (草书).

| Group   | Scripts                                                            | Tasks                                             |
| ------- | ------------------------------------------------------------------ | ------------------------------------------------- |
| Ancient | Oracle Bone / Bronze Script / Seal Script                          | Spotting · Recognition · Parsing · Classification |
| Modern  | Clerical Script / Regular Script / Running Script / Cursive Script | Parsing · Classification                          |

The four tasks:

| Task                                       | Short Name     | Metric                | Description                                                                |
| ------------------------------------------ | -------------- | --------------------- | -------------------------------------------------------------------------- |
| Cross-period Character Spotting            | Spotting       | F1 @ IoU > 0.75       | Detect bounding boxes and identify the modern character for each box       |
| Fine-grained Archaic Character Recognition | Recognition    | Exact-match Accuracy  | Identify the modern character inside a red bounding box drawn on the image |
| Ancient Text Parsing                       | Parsing        | 1 − NED (Levenshtein) | Read all characters in reading order; `[UNK]` is filtered before scoring   |
| Script Classification                      | Classification | Accuracy              | Classify the image into one of the seven canonical scripts                 |

All scoring is **rule-based** — no LLM judge is needed.

> Note: the Spotting task internally also reports a Detection F1 (bbox-only, IoU > 0.75 without character matching) as a diagnostic; the headline Spotting score requires both IoU and character match.

---

## 1. Setup

```bash
git clone <this-repo>
cd ChronoText/Opensource
pip install -r requirements.txt
# Optional: only if you plan to use --api_type local_vllm
pip install vllm
```

## 2. Download benchmark data

The dataset (jsonl + images) is released as a single archive. Place the files under `Opensource/data/`:

```
Opensource/data/
├── Chronicles_OCR.jsonl
└── images/
    ├── 甲骨文/...   # Oracle Bone
    ├── 金文/...     # Bronze Script
    ├── 篆书/...     # Seal Script
    ├── 隶书/...     # Clerical Script
    ├── 楷书/...     # Regular Script
    ├── 行书/...     # Running Script
    └── 草书/...     # Cursive Script
```

Each line of the jsonl looks like:

```json
{
  "image_path": "images/甲骨文/abcdef0123.jpg",
  "font_type": "甲骨文",
  "annotation": "...",
  "spotting": [{"bbox": {"x1":..,"y1":..,"x2":..,"y2":..}, "modern_char": ".."}, ...],
  "width": 800,
  "height": 600
}
```

`spotting` / `width` / `height` only exist for the three ancient scripts; modern scripts only carry `image_path`, `font_type`, and `annotation`.

## 3. Inference

Three backends are supported via `--api_type`:

### (a) `openai_compat` — any OpenAI-compatible HTTP service

Works with locally-served models (`vllm serve`, `sglang`, `lmdeploy`) **or** public APIs that speak the OpenAI Chat Completions protocol (OpenAI, Gemini OpenAI-compat, Claude OpenAI-compat, Together, …).

```bash
python infer.py \
    --api_type openai_compat \
    --model_name Qwen2.5-VL-7B-Instruct \
    --base_url http://127.0.0.1:8000/v1 \
    --api_key EMPTY \
    --max_workers 64
```

### (b) `local_vllm` — in-process vLLM, give it a model path

No need to start a server first. The script loads the checkpoint directly with `vllm.LLM`.

```bash
python infer.py \
    --api_type local_vllm \
    --model_path /path/to/Qwen2.5-VL-7B-Instruct \
    --tensor_parallel_size 1 \
    --max_model_len 32768
```

### Output

Each run writes one jsonl file:

```
Opensource/infer_results/<model_tag>/results.jsonl
```

`<model_tag>` defaults to `--model_name` / basename of `--model_path` / `--api_name`. You can override it with `--output_tag`.

## 4. Judging

```bash
# All models under infer_results/
python judge.py

# Specific models
python judge.py --models Qwen2.5-VL-7B-Instruct gemini-3.1-pro
```

Outputs to `Opensource/judge_results/<model_tag>/results.jsonl`. The judge step is purely rule-based and **always overwrites** previous output (it is very fast).

## 5. Summary report

```bash
python summarize.py
# → Opensource/judge_results/results_analysis.xlsx
```

The workbook has two sheets, displayed in the canonical task order **Spotting · Recognition · Parsing · Classification**:

- **Per-group summary** — per-model averages aggregated by Ancient / Modern groups
- **Per-script breakdown** — per-model averages broken down by each of the seven scripts

Scores are scaled `×100` and shown to 1 decimal (e.g. `87.3` means 0.873).

---

## 6. End-to-end example

```bash
# 1. Run inference
python infer.py --api_type openai_compat \
    --model_name Qwen2.5-VL-7B-Instruct \
    --base_url http://127.0.0.1:8000/v1

# 2. Score
python judge.py

# 3. Aggregate to Excel
python summarize.py
```

---

## 7. Repo layout

```
Opensource/
├── README.md / README_zh.md
├── requirements.txt
├── data/                            # ← download benchmark data here
├── apis/
│   ├── base.py                      # APIBase
│   ├── openai_compat.py             # OpenAI-compatible client
│   ├── local_vllm.py                # in-process vLLM
├── prompts/
│   ├── spotting.py                  # Cross-period Character Spotting
│   ├── referring.py                 # Fine-grained Archaic Character Recognition (red-box rendering)
│   ├── extract_text.py              # Ancient Text Parsing
│   └── classify.py                  # Script Classification
├── judges/
│   ├── spotting.py
│   ├── referring.py
│   ├── extract_text.py
│   └── classify.py
├── utils/
│   ├── image_utils.py               # base64 encoding for OpenAI-compat
│   ├── io.py                        # ResultWriter / read_processed
│   ├── signal_utils.py              # Ctrl+C aware shutdown
│   └── unk.py                       # [UNK] / □ / ■ etc.
├── infer.py                         # entry: inference
├── judge.py                         # entry: rule-based scoring
└── summarize.py                     # entry: Excel report
```
