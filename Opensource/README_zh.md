# Chronicles-OCR Benchmark

面向视觉语言模型（VLM）的 **中国历代书体 OCR** 多任务评测基准，覆盖全部七种规范汉字书体：甲骨文（Oracle Bone）、金文（Bronze Script）、篆书（Seal Script）、隶书（Clerical Script）、楷书（Regular Script）、行书（Running Script）、草书（Cursive Script）。

| 分组 | 书体                      | 任务                                              |
| ---- | ------------------------- | ------------------------------------------------- |
| 古代 | 甲骨文 / 金文 / 篆书      | Spotting · Recognition · Parsing · Classification |
| 近代 | 隶书 / 楷书 / 行书 / 草书 | Parsing · Classification                          |

四个任务：

| 任务                                       | 简称           | 指标                   | 说明                                             |
| ------------------------------------------ | -------------- | ---------------------- | ------------------------------------------------ |
| Cross-period Character Spotting            | Spotting       | F1 @ IoU > 0.75        | 检测每个字符的 bbox 并识别其对应的现代汉字       |
| Fine-grained Archaic Character Recognition | Recognition    | Exact-match Accuracy   | 识别图中红色矩形框内单个古文字符所对应的现代汉字 |
| Ancient Text Parsing                       | Parsing        | 1 − NED（Levenshtein） | 按阅读顺序识别图中所有汉字；评分前会过滤 `[UNK]` |
| Script Classification                      | Classification | Accuracy               | 将图像分类到七种规范书体中的其中之一             |

全部评分均为 **基于规则**，**不需要 LLM 评审**。

> 注：Spotting 任务内部还会同时报告一个 Detection F1（仅看 bbox、IoU > 0.75，不要求字符一致）作为诊断指标；Spotting 主指标要求 IoU 与字符同时命中。

---

## 1. 环境安装

```bash
git clone <this-repo>
cd ChronoText/Opensource
pip install -r requirements.txt
# 可选：仅当使用 --api_type local_vllm 时需要
pip install vllm
```

## 2. 下载评测数据

数据（jsonl + 图片）以单一压缩包发布。请将其解压到 `Opensource/data/` 目录下：

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

jsonl 每一行的格式如下：

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

`spotting` / `width` / `height` 仅在三种古代书体上存在；近代书体仅包含 `image_path`、`font_type`、`annotation`。

## 3. 推理（Inference）

通过 `--api_type` 切换三种后端：

### (a) `openai_compat` — 任意 OpenAI 兼容 HTTP 服务

适用于 `vllm serve` / `sglang` / `lmdeploy` 等本地服务，也适用于符合 OpenAI Chat Completions 协议的公有云接口（OpenAI、Gemini OpenAI-compat、Claude OpenAI-compat、Together 等）。

```bash
python infer.py \
    --api_type openai_compat \
    --model_name Qwen2.5-VL-7B-Instruct \
    --base_url http://127.0.0.1:8000/v1 \
    --api_key EMPTY \
    --max_workers 64
```

### (b) `local_vllm` — 进程内加载 vLLM，直接给本地权重路径

不需要先启动服务，脚本会通过 `vllm.LLM` 在进程内加载本地 checkpoint。

```bash
python infer.py \
    --api_type local_vllm \
    --model_path /path/to/Qwen2.5-VL-7B-Instruct \
    --tensor_parallel_size 1 \
    --max_model_len 32768
```

### 输出位置

每次运行会写入一个 jsonl：

```
Opensource/infer_results/<model_tag>/results.jsonl
```

`<model_tag>` 默认依次取 `--model_name` / `--model_path` 的 basename / `--api_name`，也可以用 `--output_tag` 显式覆盖。

## 4. 评分（Judging）

```bash
# 评分 infer_results/ 下的全部模型
python judge.py

# 只评分指定模型
python judge.py --models Qwen2.5-VL-7B-Instruct gemini-3.1-pro
```

输出到 `Opensource/judge_results/<model_tag>/results.jsonl`。评分阶段为纯规则计算、速度很快，因此 **始终覆盖** 之前的结果。

## 5. 汇总报表（Summary）

```bash
python summarize.py
# → Opensource/judge_results/results_analysis.xlsx
```

输出的 Excel 含两张表，且任务列均按规范顺序 **Spotting · Recognition · Parsing · Classification** 排列：

- **Per-group summary** — 按 Ancient / Modern 两个分组聚合的每模型平均分
- **Per-script breakdown** — 拆解到七种书体的每模型平均分

分数会乘以 `100`，保留 1 位小数（例如 `87.3` 表示 0.873）。

---

## 6. 完整流程示例

```bash
# 1. 推理
python infer.py --api_type openai_compat \
    --model_name Qwen2.5-VL-7B-Instruct \
    --base_url http://127.0.0.1:8000/v1

# 2. 评分
python judge.py

# 3. 汇总到 Excel
python summarize.py
```

---

## 7. 代码结构

```
Opensource/
├── README.md / README_zh.md
├── requirements.txt
├── data/                            # ← 数据下载到这里
├── apis/
│   ├── base.py                      # APIBase
│   ├── openai_compat.py             # OpenAI 兼容客户端
│   ├── local_vllm.py                # 进程内 vLLM
├── prompts/
│   ├── spotting.py                  # Cross-period Character Spotting
│   ├── referring.py                 # Fine-grained Archaic Character Recognition（红框采样 + 渲染）
│   ├── extract_text.py              # Ancient Text Parsing
│   └── classify.py                  # Script Classification
├── judges/
│   ├── spotting.py
│   ├── referring.py
│   ├── extract_text.py
│   └── classify.py
├── utils/
│   ├── image_utils.py               # OpenAI 兼容 API 的 base64 编码
│   ├── io.py                        # ResultWriter / read_processed
│   ├── signal_utils.py              # 友好响应 Ctrl+C
│   └── unk.py                       # [UNK] / □ / ■ 等占位归一化
├── infer.py                         # 入口：推理
├── judge.py                         # 入口：规则评分
└── summarize.py                     # 入口：Excel 报表
```
