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

### 1. Cross-period Character Spotting
- **Scope:** Oracle Bone, Bronze, Seal
- **Goal:** Simultaneously localize and decipher archaic symbols
- **Metric:** H-mean (IoU > 0.75 + exact character match)

### 2. Fine-grained Archaic Character Recognition
- **Scope:** Oracle Bone, Bronze, Seal
- **Goal:** Recognize archaic characters via visual referring (colored bounding box)
- **Metric:** Exact Match Accuracy

### 3. Ancient Text Parsing
- **Scope:** All Seven Scripts
- **Goal:** Transcribe text following original reading order
- **Metric:** Normalized Edit Distance (NED)

### 4. Script Classification
- **Scope:** All Seven Scripts
- **Goal:** Classify images into one of the seven script types
- **Metric:** Accuracy

## Key Results (Archaic Scripts)

| Model | Spotting | Fine-grained Rec. | Parsing | Classification |
|-------|:--------:|:-----------------:|:-------:|:--------------:|
| Seed 2.0 Pro | **19.8** | 24.5 | 0.26 | 95.3 |
| Kimi K2.5 | 6.7 | **31.6** | **0.28** | 95.2 |
| Qwen3.5-A17B | 9.7 | 22.6 | 0.22 | 88.3 |
| Gemini 3.1 Pro | 3.5 | 23.2 | 0.18 | 92.1 |
| GPT-5 | 0.5 | 4.2 | 0.06 | 85.5 |

> Even the most capable VLLMs struggle with archaic script perception — Spotting H-mean remains near zero for most models, revealing fundamental bottlenecks in fine-grained grounding and morphological decipherment.

## Dataset

🚧 **Dataset is being organized and will be released soon.**

<!-- 
Download links (to be updated):
- [GitHub Releases]()
- [HuggingFace Dataset]()
-->

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
