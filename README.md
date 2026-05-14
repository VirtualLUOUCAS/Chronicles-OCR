# Chronicles-OCR

**A Cross-Temporal Perception Benchmark for the Evolutionary Trajectory of Chinese Characters**

<p align="center">
  <a href="README_ZH.md">中文版</a> •
  <a href="https://arxiv.org/abs/2603.23885">Paper</a> •
  <a href="https://github.com/VirtualLUOUCAS/Chronicles-OCR">GitHub</a> •
  <a href="https://huggingface.co/datasets/VirtualLUO/Chronicles-OCR">HuggingFace</a>
</p>

## Overview

**Chronicles-OCR** is the first comprehensive benchmark specifically designed to evaluate the cross-temporal visual perception capabilities of VLLMs across the complete evolutionary trajectory of Chinese characters — the **"Seven Chinese Scripts"**.

Curated in collaboration with top-tier institutional domain experts (the Key Laboratory of Oracle Bone Inscription Information Processing at Anyang Normal University and the Palace Museum), the dataset comprises **2,800 strictly balanced images** encompassing highly diverse physical media, ranging from tortoise shells to paper-based calligraphy.

<p align="center">
  <img src="assets/overview.png" width="95%" alt="Chronicles-OCR Overview">
</p>

## The Seven Chinese Scripts

| Script | Period | Physical Media |
|--------|--------|----------------|
| Oracle Bone (甲骨文) | ~1300–1046 BCE | Tortoise shells, animal bones |
| Bronze (金文) | 1046–256 BCE | Ceremonial bronze vessels |
| Seal (篆书) | 221–200 BCE | Steles, official documents |
| Clerical (隶书) | 250 BCE–220 CE | Wooden slips, steles |
| Regular (楷书) | 150–600 CE | Paper, steles |
| Cursive (草书) | 100 BCE–700 CE | Paper, calligraphic scrolls |
| Running (行书) | 150–400 CE | Paper, calligraphic scrolls |

## Benchmark Statistics

| Item | Details |
|------|---------|
| Total Images | 2,800 (400 per script × 7 scripts) |
| Script Coverage | All Seven Chinese Scripts |
| Annotation | Stage-Adaptive: character-level for archaic, paragraph-level for mature scripts |
| Expert Partners | Anyang Normal University (Oracle Bone), Palace Museum (Clerical–Cursive) |
| Tasks | 4 evaluation tasks |

## Evaluation Tasks

| Task | Short Name | Scope | Metric |
|------|-----------|-------|--------|
| Cross-period Character Spotting | Spotting | Oracle Bone, Bronze, Seal | F1 @ IoU > 0.75 |
| Fine-grained Archaic Character Recognition | Recognition | Oracle Bone, Bronze, Seal | Exact-match Accuracy |
| Ancient Text Parsing | Parsing | All Seven Scripts | 1 − NED (Levenshtein) |
| Script Classification | Classification | All Seven Scripts | Accuracy |

## 🏆 Leaderboard

### Archaic Scripts (Oracle Bone, Bronze, Seal)

| Model | Think | Avg Spot. | Avg Fine. | Avg Pars. | Avg Class. | OB Spot. | OB Fine. | OB Pars. | OB Class. | Br Spot. | Br Fine. | Br Pars. | Br Class. | Se Spot. | Se Fine. | Se Pars. | Se Class. |
|:------|:-----:|:---------:|:---------:|:---------:|:----------:|:--------:|:--------:|:--------:|:---------:|:--------:|:--------:|:--------:|:---------:|:--------:|:--------:|:--------:|:---------:|
| **Open-Source Models** | | | | | | | | | | | | | | | | | |
| InternVL3.5-8B | | 0.1 | 6.0 | 0.07 | 56.7 | 0.0 | 1.1 | 0.01 | 86.2 | 0.0 | 2.2 | 0.03 | 7.0 | 0.2 | 14.5 | 0.17 | 77.0 |
| InternVL3.5-A28B | | 0.5 | 15.7 | 0.13 | 79.0 | 0.0 | 2.5 | 0.02 | 96.3 | 0.4 | 7.8 | 0.08 | 79.2 | 1.0 | 36.8 | 0.29 | 61.5 |
| Qwen2.5-VL-7B | | 0.0 | 7.4 | 0.07 | 71.8 | 0.0 | 4.0 | 0.02 | 93.8 | 0.0 | 4.5 | 0.04 | 22.5 | 0.0 | 13.8 | 0.14 | 99.2 |
| Qwen2.5-VL-72B | | 0.0 | 0.0 | 0.07 | 74.2 | 0.0 | 0.0 | 0.01 | 98.0 | 0.0 | 0.0 | 0.04 | 26.0 | 0.0 | 0.0 | 0.16 | 98.5 |
| Qwen3-VL-2B | | 2.1 | 10.7 | 0.12 | 73.0 | 0.0 | 1.4 | 0.00 | 96.6 | 0.8 | 6.8 | 0.06 | 36.5 | 5.7 | 24.0 | 0.31 | 85.8 |
| Qwen3-VL-8B | | 3.4 | 17.3 | 0.18 | 73.7 | 0.2 | 3.4 | 0.01 | 98.6 | 2.5 | 11.0 | 0.10 | 24.0 | 7.5 | 37.5 | 0.42 | 98.5 |
| Qwen3-VL-8B | ✓ | 1.0 | 9.1 | 0.09 | 67.3 | 0.0 | 3.7 | 0.03 | 97.7 | 0.2 | 7.0 | 0.05 | 31.8 | 2.8 | 16.8 | 0.20 | 72.5 |
| Qwen3-VL-A22B | | 7.8 | 17.5 | 0.19 | 91.8 | 0.3 | 5.4 | 0.01 | 99.2 | 6.5 | 12.2 | 0.12 | 80.2 | 16.6 | 35.0 | 0.43 | 96.0 |
| Qwen3-VL-A22B | ✓ | 2.1 | 13.6 | 0.17 | 87.3 | 0.1 | 4.2 | 0.03 | 98.0 | 0.9 | 10.2 | 0.11 | 66.8 | 5.3 | 26.2 | 0.37 | 97.2 |
| Qwen3.5-A3B | | 5.6 | 16.2 | 0.20 | 76.5 | 0.2 | 5.1 | 0.02 | 99.7 | 5.3 | 11.5 | 0.12 | 30.0 | 11.2 | 32.0 | 0.45 | **99.8** |
| Qwen3.5-A17B | | 9.7 | 22.6 | 0.22 | 88.3 | 0.5 | 9.1 | 0.02 | 99.7 | 9.2 | 17.5 | 0.13 | 67.2 | 19.4 | 41.3 | 0.50 | 98.0 |
| Gemma 4 31B it | | 2.3 | 7.0 | 0.04 | 70.0 | 0.0 | 3.1 | 0.01 | 72.6 | 1.0 | 6.5 | 0.03 | 74.8 | 6.0 | 11.2 | 0.10 | 62.7 |
| MiniCPM-V 4.5 | ✓ | 0.0 | 4.8 | 0.02 | 73.8 | 0.0 | 2.5 | 0.01 | 95.2 | 0.0 | 5.5 | 0.03 | 18.0 | 0.1 | 9.0 | 0.04 | 82.5 |
| Molmo 7B-D 0924 | | 0.0 | 0.1 | 0.00 | 24.2 | 0.0 | 0.0 | 0.01 | 40.8 | 0.0 | 0.2 | 0.00 | 0.0 | 0.0 | 0.0 | 0.00 | 20.5 |
| Molmo 72B 0924 | | 0.0 | 0.3 | 0.00 | 34.7 | 0.0 | 0.5 | 0.00 | 28.0 | 0.0 | 0.5 | 0.00 | 0.8 | 0.0 | 0.0 | 0.00 | 82.0 |
| Ovis2.6-30B-A3B | ✓ | 1.9 | 9.0 | 0.09 | 68.3 | 0.1 | 2.0 | 0.01 | 89.8 | 0.7 | 7.5 | 0.06 | 13.5 | 6.8 | 24.5 | 0.25 | 79.0 |
| GLM-4.5V 108B | ✓ | 1.4 | 6.1 | 0.05 | 76.8 | 0.1 | 4.2 | 0.03 | **100** | 2.0 | 6.5 | 0.05 | 15.5 | 3.3 | 9.2 | 0.10 | 91.5 |
| Kimi K2.5 | | 5.0 | **27.1** | **0.22** | 96.4 | 0.1 | 11.5 | 0.05 | **100** | 7.5 | 25.8 | 0.19 | 90.0 | 12.5 | **58.5** | **0.60** | 95.5 |
| Kimi K2.5 | ✓ | 1.8 | 20.3 | 0.22 | 94.7 | 0.0 | 10.2 | **0.05** | 99.8 | 1.2 | 17.5 | 0.20 | 85.8 | 6.0 | 44.8 | 0.57 | 93.5 |
| **Proprietary Models** | | | | | | | | | | | | | | | | | |
| GPT-4o | | 0.1 | 1.5 | 0.02 | 82.0 | 0.0 | 0.5 | 0.01 | 96.5 | 0.0 | 1.0 | 0.02 | 46.8 | 0.3 | 4.5 | 0.06 | 89.0 |
| GPT-5 | | 0.4 | 3.7 | 0.04 | 88.1 | 0.0 | 4.0 | 0.00 | 98.2 | 0.0 | 4.0 | 0.04 | 60.5 | 1.6 | 4.5 | 0.12 | 97.5 |
| Seed 1.8 | | 9.2 | 20.6 | 0.16 | 94.7 | 0.4 | 9.2 | 0.03 | 99.5 | 9.4 | 15.8 | 0.17 | 80.5 | 26.7 | 45.0 | 0.42 | 99.0 |
| Seed 1.8 | ✓ | 7.4 | 17.1 | 0.17 | **96.7** | 0.4 | 8.8 | 0.04 | 99.5 | 5.8 | 14.8 | 0.18 | 90.0 | 23.3 | 36.2 | 0.43 | 97.5 |
| Seed 2.0 Pro | | **16.5** | 24.5 | 0.18 | 95.9 | **3.0** | 11.0 | 0.03 | 99.5 | **19.9** | **30.8** | 0.22 | **92.2** | **40.7** | 41.5 | 0.43 | 93.8 |
| Seed 2.0 Pro | ✓ | 15.3 | 23.3 | 0.21 | 96.6 | 2.4 | 11.2 | 0.04 | 99.8 | 17.8 | 26.0 | **0.26** | **92.2** | 39.1 | 37.5 | 0.49 | 94.5 |
| MiMo-V2-Omni | ✓ | 0.4 | 8.6 | 0.08 | 87.7 | 0.0 | 6.5 | 0.04 | 99.5 | 0.2 | 8.0 | 0.07 | 58.5 | 1.5 | 9.8 | 0.15 | 93.0 |
| Gemini 2.5 Pro | ✓ | 0.8 | 7.5 | 0.07 | 87.5 | 0.0 | 5.8 | 0.04 | 99.5 | 0.2 | 7.0 | 0.06 | 80.5 | 2.8 | 10.8 | 0.14 | 70.2 |
| Gemini 3.1 Pro | ✓ | 2.6 | 19.5 | 0.15 | 93.8 | 0.0 | **14.0** | 0.05 | 99.5 | 2.5 | 22.5 | 0.18 | 84.5 | 7.8 | 32.2 | 0.32 | 93.2 |
| Claude Opus 4.7 | ✓ | 0.4 | 10.0 | 0.08 | 90.4 | 0.0 | 4.8 | 0.03 | 93.8 | 0.1 | 9.5 | 0.05 | 80.5 | 1.4 | 21.5 | 0.21 | 93.8 |

> **OB** = Oracle Bone, **Br** = Bronze, **Se** = Seal. **Bold** = best, scores are H-mean (Spot.), Accuracy (Fine./Class.), NED (Pars.).

### Mature Scripts (Clerical, Regular, Running, Cursive)

| Model | Think | Avg Pars. | Avg Class. | Cl Pars. | Cl Class. | Re Pars. | Re Class. | Ru Pars. | Ru Class. | Cu Pars. | Cu Class. |
|:------|:-----:|:---------:|:----------:|:--------:|:---------:|:--------:|:---------:|:--------:|:---------:|:--------:|:---------:|
| **Open-Source Models** | | | | | | | | | | | |
| InternVL3.5-8B | | 0.40 | 35.6 | 0.41 | 1.8 | 0.51 | 69.4 | 0.38 | 52.9 | 0.30 | 35.0 |
| InternVL3.5-A28B | | 0.56 | 58.1 | 0.54 | 28.5 | 0.69 | 85.5 | 0.56 | 63.3 | 0.46 | 75.2 |
| Qwen2.5-VL-7B | | 0.44 | 34.8 | 0.54 | 8.0 | 0.62 | 17.0 | 0.42 | 36.4 | 0.21 | 90.5 |
| Qwen2.5-VL-72B | | 0.49 | 57.2 | 0.59 | 18.0 | 0.66 | 91.5 | 0.46 | 56.6 | 0.26 | 86.0 |
| Qwen3-VL-2B | | 0.57 | 35.2 | 0.61 | 5.5 | 0.71 | 11.8 | 0.50 | 37.9 | 0.42 | 93.0 |
| Qwen3-VL-8B | | 0.66 | 60.9 | 0.69 | 32.5 | 0.77 | **97.2** | 0.64 | 59.1 | 0.56 | 81.0 |
| Qwen3-VL-8B | ✓ | 0.49 | 45.9 | 0.52 | 11.2 | 0.64 | 79.7 | 0.51 | 53.4 | 0.32 | 56.2 |
| Qwen3-VL-A22B | | 0.66 | 64.9 | 0.69 | 36.5 | 0.73 | 95.5 | 0.66 | 68.3 | 0.59 | 82.0 |
| Qwen3-VL-A22B | ✓ | 0.65 | 60.4 | 0.67 | 31.0 | 0.75 | 93.5 | 0.65 | 62.3 | 0.54 | 78.0 |
| Qwen3.5-A3B | | 0.71 | 68.1 | 0.79 | 36.8 | 0.81 | 84.2 | 0.68 | 75.6 | 0.57 | 84.2 |
| Qwen3.5-A17B | | **0.73** | 72.2 | **0.81** | 52.0 | 0.81 | 81.3 | 0.67 | 75.3 | 0.66 | 89.4 |
| Gemma 4 31B it | | 0.34 | 57.1 | 0.37 | 9.6 | 0.56 | 81.9 | 0.33 | 65.0 | 0.09 | 84.5 |
| MiniCPM-V 4.5 | ✓ | 0.40 | 44.9 | 0.45 | 2.8 | 0.61 | 87.5 | 0.38 | 56.9 | 0.15 | 48.8 |
| Molmo 7B-D 0924 | | 0.01 | 16.9 | 0.01 | **70.8** | 0.01 | 3.0 | 0.01 | 0.7 | 0.01 | 0.5 |
| Molmo 72B 0924 | | 0.00 | 9.1 | 0.00 | 6.8 | 0.01 | 16.5 | 0.01 | 3.2 | 0.00 | 12.8 |
| Ovis2.6-30B-A3B | ✓ | 0.53 | 39.7 | 0.54 | 8.5 | 0.63 | 77.9 | 0.57 | 71.6 | 0.42 | 12.2 |
| GLM-4.5V 108B | ✓ | 0.44 | 56.6 | 0.45 | 11.5 | 0.61 | 84.5 | 0.44 | 63.3 | 0.23 | 81.5 |
| Kimi K2.5 | | 0.71 | **77.0** | 0.73 | 70.2 | 0.78 | 78.2 | 0.72 | 77.8 | 0.66 | 86.0 |
| Kimi K2.5 | ✓ | 0.70 | 72.3 | 0.75 | 68.5 | 0.78 | 81.7 | 0.60 | 65.3 | **0.66** | 84.8 |
| **Proprietary Models** | | | | | | | | | | | |
| GPT-4o | | 0.30 | 55.9 | 0.35 | 20.5 | 0.47 | 83.0 | 0.24 | 55.6 | 0.12 | 80.5 |
| GPT-5 | | 0.38 | 62.1 | 0.50 | 36.2 | 0.57 | 59.6 | 0.21 | **78.1** | 0.18 | 71.0 |
| Seed 1.8 | | 0.69 | 69.6 | 0.68 | 45.5 | 0.79 | 92.7 | 0.69 | 71.8 | 0.61 | 82.5 |
| Seed 1.8 | ✓ | 0.67 | 71.1 | 0.69 | 48.0 | 0.78 | 89.2 | 0.57 | 73.3 | 0.60 | 80.8 |
| Seed 2.0 Pro | | 0.72 | 76.1 | 0.75 | 60.8 | 0.81 | 82.0 | **0.73** | 77.6 | 0.62 | 92.2 |
| Seed 2.0 Pro | ✓ | 0.71 | 75.3 | 0.76 | 61.8 | 0.80 | 82.0 | 0.65 | 74.3 | 0.66 | 89.0 |
| MiMo-V2-Omni | ✓ | 0.56 | 62.3 | 0.62 | 40.0 | 0.71 | 80.7 | 0.58 | 73.3 | 0.36 | 64.2 |
| Gemini 2.5 Pro | ✓ | 0.53 | 56.3 | 0.67 | 33.2 | 0.72 | 39.6 | 0.49 | 59.4 | 0.23 | 95.0 |
| Gemini 3.1 Pro | ✓ | 0.70 | 73.1 | 0.80 | 61.0 | **0.83** | 62.7 | 0.66 | 71.1 | 0.52 | **95.8** |
| Claude Opus 4.7 | ✓ | 0.50 | 66.8 | 0.53 | 50.2 | 0.63 | 74.4 | 0.44 | 56.6 | 0.38 | 86.0 |

> **Cl** = Clerical, **Re** = Regular, **Ru** = Running, **Cu** = Cursive. **Bold** = best.

## Getting Started

### 1. Setup

```bash
git clone https://github.com/VirtualLUOUCAS/Chronicles-OCR.git
cd Chronicles-OCR
pip install -r requirements.txt
```

### 2. Download Data

Download and place the benchmark data under `data/`:

```
data/
├── Chronicles_OCR.jsonl
└── images/
    ├── 甲骨文/    # Oracle Bone
    ├── 金文/      # Bronze Script
    ├── 篆书/      # Seal Script
    ├── 隶书/      # Clerical Script
    ├── 楷书/      # Regular Script
    ├── 行书/      # Running Script
    └── 草书/      # Cursive Script
```

### 3. Inference

```bash
# OpenAI-compatible API
python infer.py --api_type openai_compat \
    --model_name Qwen2.5-VL-7B-Instruct \
    --base_url http://127.0.0.1:8000/v1 \
    --api_key EMPTY --max_workers 64

# Local vLLM
python infer.py --api_type local_vllm \
    --model_path /path/to/model \
    --tensor_parallel_size 1 --max_model_len 32768
```

### 4. Judging (Rule-based)

```bash
python judge.py                    # all models
python judge.py --models model_a   # specific model
```

### 5. Summary Report

```bash
python summarize.py
# → judge_results/results_analysis.xlsx
```

## Citation

```bibtex
@misc{li2026chronicles,
      title={Chronicles-OCR: A Cross-Temporal Perception Benchmark for the Evolutionary Trajectory of Chinese Characters},
      author={Gengluo Li and Shangping Peng and Xingyu Wan and Chengquan Zhang and Hao Feng and Xin Xu and Pian Wu and Bang Li and Zengmao Ding and Yongge Liu and Yipei Ye and Yang Yang and Zhan Shu and Guojun Yan and Zhe Li and Can Ma and Weiping Wang and Yu Zhou and Han Hu},
      year={2026},
      journal={arXiv preprint arXiv:2603.23885},
      url={https://arxiv.org/abs/2603.23885},
}
```

## Acknowledgements

We sincerely acknowledge the Key Laboratory of Oracle Bone Inscription Information Processing at Anyang Normal University and the Palace Museum for their invaluable contributions to data sourcing and expert annotation.

## License

This benchmark is released for **research purposes only**.
