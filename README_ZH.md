# Chronicles-OCR

**汉字演化轨迹的跨时域感知基准**

<p align="center">
  <a href="README.md">English</a> •
  <a href="https://arxiv.org/abs/2603.23885">论文</a> •
  <a href="https://github.com/VirtualLUOUCAS/Chronicles-OCR">GitHub</a> •
  <a href="https://huggingface.co/datasets/VirtualLUO/Chronicles-OCR">HuggingFace</a>
</p>

## 概述

**Chronicles-OCR** 是首个专为评估视觉语言大模型（VLLMs）跨时域视觉感知能力而设计的综合性基准，覆盖汉字完整的演化轨迹——**"汉字七体"**。

本数据集与安阳师范学院甲骨文信息处理教育部重点实验室及故宫博物院等顶级机构领域专家合作构建，包含 **2,800 张严格均衡的图像**，涵盖从龟甲到纸本书法在内的高度多样化物理媒介。

<p align="center">
  <img src="assets/overview.png" width="95%" alt="Chronicles-OCR 概览">
</p>

## 汉字七体

| 书体 | 年代 | 物理载体 |
|------|------|----------|
| 甲骨文 | 约公元前1300–1046年 | 龟甲、兽骨 |
| 金文 | 公元前1046–256年 | 青铜礼器 |
| 篆书 | 公元前221–200年 | 碑刻、官方文书 |
| 隶书 | 公元前250年–公元220年 | 木简、碑刻 |
| 楷书 | 公元150–600年 | 纸本、碑刻 |
| 草书 | 公元前100年–公元700年 | 纸本、书法长卷 |
| 行书 | 公元150–400年 | 纸本、书法长卷 |

## 基准统计

| 项目 | 详情 |
|------|------|
| 图片总数 | 2,800（每种书体 400 张 × 7 种书体） |
| 书体覆盖 | 汉字七体全覆盖 |
| 标注方式 | 阶段自适应：古体为字符级，成熟书体为段落级 |
| 专家合作方 | 安阳师范学院（甲骨文）、故宫博物院（隶书–草书） |
| 评测任务 | 4 项评测任务 |

## 评测任务

### 1. 跨时期字符检测（Cross-period Character Spotting）
- **适用范围：** 甲骨文、金文、篆书
- **目标：** 同时定位和识别古体符号
- **指标：** H-mean（IoU > 0.75 + 精确字符匹配）

### 2. 细粒度古文字识别（Fine-grained Archaic Character Recognition）
- **适用范围：** 甲骨文、金文、篆书
- **目标：** 通过视觉指示（彩色边框标注）识别古文字
- **指标：** 精确匹配准确率（Exact Match Accuracy）

### 3. 古文本解析（Ancient Text Parsing）
- **适用范围：** 七种书体
- **目标：** 按原始阅读顺序转录文本
- **指标：** 归一化编辑距离（NED）

### 4. 书体分类（Script Classification）
- **适用范围：** 七种书体
- **目标：** 将图像分类为七种书体之一
- **指标：** 准确率（Accuracy）

## 主要结果（古体书法）

| 模型 | 字符检测 | 细粒度识别 | 文本解析 | 书体分类 |
|------|:--------:|:---------:|:-------:|:-------:|
| Seed 2.0 Pro | **19.8** | 24.5 | 0.26 | 95.3 |
| Kimi K2.5 | 6.7 | **31.6** | **0.28** | 95.2 |
| Qwen3.5-A17B | 9.7 | 22.6 | 0.22 | 88.3 |
| Gemini 3.1 Pro | 3.5 | 23.2 | 0.18 | 92.1 |
| GPT-5 | 0.5 | 4.2 | 0.06 | 85.5 |

> 即使是最先进的 VLLMs 在古体文字感知上也表现挣扎——绝大多数模型的字符检测 H-mean 接近零，揭示了细粒度视觉定位与形态辨识方面的根本性瓶颈。

## 数据集

🚧 **数据集正在整理中，将于近期发布。**

<!-- 
下载链接（待更新）：
- [GitHub Releases]()
- [HuggingFace Dataset]()
-->

## 引用

```bibtex
@misc{li2026chronicles,
      title={Chronicles-OCR: A Cross-Temporal Perception Benchmark for the Evolutionary Trajectory of Chinese Characters},
      author={Gengluo Li and Shangping Peng and Xingyu Wan and Chengquan Zhang and Hao Feng and Xin Xu and Pian Wu and Bang Li and Zengmao Ding and Yongge Liu and Yipei Ye and Yang Yang and Zhan Shu and Guojun Yan and Zhe Li and Can Ma and Weiping Wang and Yu Zhou and Han Hu},
      year={2026},
      journal={arXiv preprint arXiv:2603.23885},
      url={https://arxiv.org/abs/2603.23885},
}
```

## 致谢

衷心感谢安阳师范学院甲骨文信息处理教育部重点实验室和故宫博物院在数据来源和专家标注方面的宝贵贡献。

## 许可

本基准仅供**学术研究**使用。
