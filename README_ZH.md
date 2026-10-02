# Chronicles-OCR

**汉字演化轨迹的跨时域感知基准**

<p align="center">
  <a href="README.md">English</a> •
  <a href="https://arxiv.org/abs/2605.11960">论文</a> •
  <strong><a href="#-排行榜">排行榜</a></strong> •
  <a href="https://github.com/VirtualLUOUCAS/Chronicles-OCR">GitHub</a> •
  <a href="https://huggingface.co/datasets/VirtualLUO/Chronicles-OCR">HuggingFace</a> •
  <a href="https://modelscope.cn/datasets/VirtualLUO/Chronicles-OCR">ModelScope</a>
</p>

## 概述

**Chronicles-OCR** 是首个专为评估视觉语言大模型（VLLMs）跨时域视觉感知能力而设计的综合性基准，覆盖汉字完整的演化轨迹——**"汉字七体"**。

本数据集与安阳师范学院甲骨文信息处理教育部重点实验室及故宫博物院等顶级机构领域专家合作构建，包含 **2,800 张严格均衡的图像**，涵盖从龟甲到纸本书法在内的高度多样化物理媒介。

<p align="center">
  <img src="assets/overview.png" width="95%" alt="Chronicles-OCR 概览">
</p>

## 汉字七体

**"汉字七体"** 是指汉字在五千余年演变历程中出现的七种代表性字体：

1. **甲骨文** — 殷商时代刻写在龟甲兽骨上的文字，是中国已知最早的成熟汉字。象形性较强，写法不固定，由细瘦线条构成，多直笔，外形参差不齐。
2. **金文（钟鼎文）** — 主要在商周时期铸刻于青铜礼器之上。笔画粗而宽，点画圆浑，体势雍容，比甲骨文更为规范，结构更加整齐。
3. **篆书** — 秦统一六国后推行的标准字体。笔画圆转，具有显著的曲线对称性和固定的结构模式，标志着从各地异体到统一书写体系的转变。
4. **隶书** — 产生于秦汉之际，字形扁平，以方折棱角取代了圆转笔画，形成"一波三折、蚕头燕尾"的特征。隶书是汉字演变史上的重要转折点，是古文字与今文字的分水岭。
5. **楷书** — 兴于汉末魏晋，字形方正，笔画规整平直，书写简便。自南北朝后成为主导字体，通行至今。
6. **草书** — 为快速书写而生的辅助性字体。笔画连带、结体简约、气势连贯，从章草到今草再到狂草，字形日趋奔放，常消除独立字符边界。
7. **行书** — 介于楷书与草书之间的流畅书体，兼具可读性与书写效率，自东汉末年产生并沿用至今。王羲之《兰亭集序》为其最负盛名的代表作。

其中，前五体（甲骨文→楷书）先后作为各自时代的正式书写系统，而草书与行书主要作为非正式场合的辅助性字体发展演变。

## 基准统计

| 项目       | 详情                                            |
| ---------- | ----------------------------------------------- |
| 图片总数   | 2,800（每种书体 400 张 × 7 种书体）             |
| 书体覆盖   | 汉字七体全覆盖                                  |
| 标注方式   | 阶段自适应：古体为字符级，成熟书体为段落级      |
| 专家合作方 | 安阳师范学院（甲骨文）、故宫博物院（隶书–草书） |
| 评测任务   | 4 项评测任务                                    |

## 评测任务

| 任务             | 简称           | 适用范围           | 指标            |
| ---------------- | -------------- | ------------------ | --------------- |
| 跨时期字符检测   | Spotting       | 甲骨文、金文、篆书 | F1 @ IoU ≥ 0.75 |
| 细粒度古文字识别 | Recognition    | 甲骨文、金文、篆书 | 精确匹配准确率  |
| 古文本解析       | Parsing        | 七种书体           | 1 − NED         |
| 书体分类         | Classification | 七种书体           | 准确率          |

## 🏆 排行榜

Chronicles-OCR 维护两个互补的多任务排行榜。古文字榜包含 Spotting、Recognition、Parsing 和 Classification，成熟书体榜包含 Parsing 和 Classification。

> **榜单更新。** 我们会定期扩充 Leaderboard 中的评测模型。也欢迎开发者将模型推理结果发送至 [ligengluo@iie.ac.cn](mailto:ligengluo@iie.ac.cn)，以便更及时地纳入评测。我们会按照官方评测协议完成适配、指标验证与榜单更新。
>
> 🏆 表示该任务在全部模型中的最佳平均结果，并列第一均保留奖杯。Thinking 与非 Thinking 模式视为不同模型配置。

### 古文字排行榜

<p align="center">
  <img src="assets/leaderboard_archaic.svg" width="100%" alt="古文字书体排行榜">
</p>

<details>
<summary><strong>查看各书体详细结果</strong></summary>

<h4>Oracle Bone Script · 甲骨文</h4>
<p align="center">
  <img src="assets/leaderboard_oracle_bone.svg" width="100%" alt="Oracle Bone Script · 甲骨文">
</p>

<h4>Bronze Script · 金文</h4>
<p align="center">
  <img src="assets/leaderboard_bronze.svg" width="100%" alt="Bronze Script · 金文">
</p>

<h4>Seal Script · 篆书</h4>
<p align="center">
  <img src="assets/leaderboard_seal.svg" width="100%" alt="Seal Script · 篆书">
</p>

<details>
<summary><strong>查看原始 HTML 表格</strong></summary>

<table>
  <thead>
    <tr>
      <th width="210" rowspan="2" align="left">模型</th>
      <th rowspan="2" align="center">Think</th>
      <th colspan="4" align="center">平均</th>
      <th colspan="4" align="center">甲骨文</th>
      <th colspan="4" align="center">金文</th>
      <th colspan="4" align="center">篆书</th>
    </tr>
    <tr>
      <th align="center">Spot.</th>
      <th align="center">Fine.</th>
      <th align="center">Pars.</th>
      <th align="center">Class.</th>
      <th align="center">Spot.</th>
      <th align="center">Fine.</th>
      <th align="center">Pars.</th>
      <th align="center">Class.</th>
      <th align="center">Spot.</th>
      <th align="center">Fine.</th>
      <th align="center">Pars.</th>
      <th align="center">Class.</th>
      <th align="center">Spot.</th>
      <th align="center">Fine.</th>
      <th align="center">Pars.</th>
      <th align="center">Class.</th>
    </tr>
  </thead>
  <tbody>
    <tr><td colspan="18" align="left"><em><strong>开源模型</strong></em></td></tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/intern.png" width="14" height="14" alt="InternVL">&#8288;&nbsp;InternVL3.5&#8209;8B</sub></td>
      <td align="center"></td>
      <td align="center">0.1</td>
      <td align="center">5.9</td>
      <td align="center">0.07</td>
      <td align="center">56.6</td>
      <td align="center">0.0</td>
      <td align="center">1.0</td>
      <td align="center">0.01</td>
      <td align="center">85.8</td>
      <td align="center">0.0</td>
      <td align="center">2.2</td>
      <td align="center">0.03</td>
      <td align="center">7.0</td>
      <td align="center">0.2</td>
      <td align="center">14.5</td>
      <td align="center">0.17</td>
      <td align="center">77.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/intern.png" width="14" height="14" alt="InternVL">&#8288;&nbsp;InternVL3.5&#8209;A28B</sub></td>
      <td align="center"></td>
      <td align="center">0.5</td>
      <td align="center">15.7</td>
      <td align="center">0.13</td>
      <td align="center">79.0</td>
      <td align="center">0.0</td>
      <td align="center">2.5</td>
      <td align="center">0.02</td>
      <td align="center">96.3</td>
      <td align="center">0.4</td>
      <td align="center">7.8</td>
      <td align="center">0.08</td>
      <td align="center">79.2</td>
      <td align="center">1.0</td>
      <td align="center">36.8</td>
      <td align="center">0.29</td>
      <td align="center">61.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen2.5&#8209;VL&#8209;7B</sub></td>
      <td align="center"></td>
      <td align="center">0.0</td>
      <td align="center">7.4</td>
      <td align="center">0.07</td>
      <td align="center">71.8</td>
      <td align="center">0.0</td>
      <td align="center">4.0</td>
      <td align="center">0.03</td>
      <td align="center">93.8</td>
      <td align="center">0.0</td>
      <td align="center">4.5</td>
      <td align="center">0.04</td>
      <td align="center">22.5</td>
      <td align="center">0.0</td>
      <td align="center">13.8</td>
      <td align="center">0.14</td>
      <td align="center">99.2</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen2.5&#8209;VL&#8209;72B</sub></td>
      <td align="center"></td>
      <td align="center">0.0</td>
      <td align="center">0.0</td>
      <td align="center">0.07</td>
      <td align="center">74.2</td>
      <td align="center">0.0</td>
      <td align="center">0.0</td>
      <td align="center">0.01</td>
      <td align="center">98.0</td>
      <td align="center">0.0</td>
      <td align="center">0.0</td>
      <td align="center">0.04</td>
      <td align="center">26.0</td>
      <td align="center">0.0</td>
      <td align="center">0.0</td>
      <td align="center">0.16</td>
      <td align="center">98.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3&#8209;VL&#8209;2B</sub></td>
      <td align="center"></td>
      <td align="center">2.1</td>
      <td align="center">10.7</td>
      <td align="center">0.12</td>
      <td align="center">73.0</td>
      <td align="center">0.0</td>
      <td align="center">1.4</td>
      <td align="center">0.00</td>
      <td align="center">96.6</td>
      <td align="center">0.8</td>
      <td align="center">6.8</td>
      <td align="center">0.06</td>
      <td align="center">36.5</td>
      <td align="center">5.7</td>
      <td align="center">24.0</td>
      <td align="center">0.31</td>
      <td align="center">85.8</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3&#8209;VL&#8209;8B</sub></td>
      <td align="center"></td>
      <td align="center">3.4</td>
      <td align="center">17.3</td>
      <td align="center">0.18</td>
      <td align="center">73.7</td>
      <td align="center">0.2</td>
      <td align="center">3.4</td>
      <td align="center">0.01</td>
      <td align="center">98.6</td>
      <td align="center">2.5</td>
      <td align="center">11.0</td>
      <td align="center">0.10</td>
      <td align="center">24.0</td>
      <td align="center">7.5</td>
      <td align="center">37.5</td>
      <td align="center">0.42</td>
      <td align="center">98.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3&#8209;VL&#8209;8B</sub></td>
      <td align="center">✓</td>
      <td align="center">1.0</td>
      <td align="center">9.1</td>
      <td align="center">0.10</td>
      <td align="center">67.3</td>
      <td align="center">0.0</td>
      <td align="center">3.7</td>
      <td align="center">0.04</td>
      <td align="center">97.7</td>
      <td align="center">0.2</td>
      <td align="center">7.0</td>
      <td align="center">0.05</td>
      <td align="center">31.8</td>
      <td align="center">2.8</td>
      <td align="center">16.8</td>
      <td align="center">0.20</td>
      <td align="center">72.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3&#8209;VL&#8209;A22B</sub></td>
      <td align="center"></td>
      <td align="center">7.8</td>
      <td align="center">17.5</td>
      <td align="center">0.19</td>
      <td align="center">91.8</td>
      <td align="center">0.3</td>
      <td align="center">5.4</td>
      <td align="center">0.02</td>
      <td align="center">99.2</td>
      <td align="center">6.5</td>
      <td align="center">12.2</td>
      <td align="center">0.12</td>
      <td align="center">80.2</td>
      <td align="center">16.6</td>
      <td align="center">35.0</td>
      <td align="center">0.43</td>
      <td align="center">96.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3&#8209;VL&#8209;A22B</sub></td>
      <td align="center">✓</td>
      <td align="center">2.1</td>
      <td align="center">13.6</td>
      <td align="center">0.17</td>
      <td align="center">87.3</td>
      <td align="center">0.1</td>
      <td align="center">4.2</td>
      <td align="center">0.04</td>
      <td align="center">98.0</td>
      <td align="center">0.9</td>
      <td align="center">10.2</td>
      <td align="center">0.11</td>
      <td align="center">66.8</td>
      <td align="center">5.3</td>
      <td align="center">26.2</td>
      <td align="center">0.38</td>
      <td align="center">97.2</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3.5&#8209;A3B</sub></td>
      <td align="center"></td>
      <td align="center">5.6</td>
      <td align="center">16.2</td>
      <td align="center">0.20</td>
      <td align="center">76.5</td>
      <td align="center">0.2</td>
      <td align="center">5.1</td>
      <td align="center">0.03</td>
      <td align="center">99.7</td>
      <td align="center">5.3</td>
      <td align="center">11.5</td>
      <td align="center">0.12</td>
      <td align="center">30.0</td>
      <td align="center">11.2</td>
      <td align="center">32.0</td>
      <td align="center">0.45</td>
      <td align="center"><strong>99.8</strong></td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3.5&#8209;A17B</sub></td>
      <td align="center"></td>
      <td align="center">9.7</td>
      <td align="center">22.6</td>
      <td align="center">0.22</td>
      <td align="center">88.3</td>
      <td align="center">0.5</td>
      <td align="center">9.1</td>
      <td align="center">0.03</td>
      <td align="center">99.7</td>
      <td align="center">9.2</td>
      <td align="center">17.5</td>
      <td align="center">0.13</td>
      <td align="center">67.2</td>
      <td align="center">19.4</td>
      <td align="center">41.3</td>
      <td align="center">0.50</td>
      <td align="center">98.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/gemma.png" width="14" height="14" alt="Gemma">&#8288;&nbsp;Gemma&nbsp;4&nbsp;31B&nbsp;it</sub></td>
      <td align="center"></td>
      <td align="center">2.3</td>
      <td align="center">7.0</td>
      <td align="center">0.05</td>
      <td align="center">70.0</td>
      <td align="center">0.0</td>
      <td align="center">3.1</td>
      <td align="center">0.01</td>
      <td align="center">72.6</td>
      <td align="center">1.0</td>
      <td align="center">6.5</td>
      <td align="center">0.03</td>
      <td align="center">74.8</td>
      <td align="center">6.0</td>
      <td align="center">11.2</td>
      <td align="center">0.10</td>
      <td align="center">62.7</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/minicpm.png" width="14" height="14" alt="MiniCPM">&#8288;&nbsp;MiniCPM&#8209;V&nbsp;4.5</sub></td>
      <td align="center">✓</td>
      <td align="center">0.0</td>
      <td align="center">5.7</td>
      <td align="center">0.03</td>
      <td align="center">65.2</td>
      <td align="center">0.0</td>
      <td align="center">2.5</td>
      <td align="center">0.01</td>
      <td align="center">95.2</td>
      <td align="center">0.0</td>
      <td align="center">5.5</td>
      <td align="center">0.03</td>
      <td align="center">18.0</td>
      <td align="center">0.1</td>
      <td align="center">9.0</td>
      <td align="center">0.04</td>
      <td align="center">82.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/AllenAI.png" width="14" height="14" alt="AllenAI">&#8288;&nbsp;Molmo&nbsp;7B&#8209;D&nbsp;0924</sub></td>
      <td align="center"></td>
      <td align="center">0.0</td>
      <td align="center">0.1</td>
      <td align="center">0.00</td>
      <td align="center">20.4</td>
      <td align="center">0.0</td>
      <td align="center">0.0</td>
      <td align="center">0.01</td>
      <td align="center">40.8</td>
      <td align="center">0.0</td>
      <td align="center">0.2</td>
      <td align="center">0.00</td>
      <td align="center">0.0</td>
      <td align="center">0.0</td>
      <td align="center">0.0</td>
      <td align="center">0.00</td>
      <td align="center">20.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/AllenAI.png" width="14" height="14" alt="AllenAI">&#8288;&nbsp;Molmo&nbsp;72B&nbsp;0924</sub></td>
      <td align="center"></td>
      <td align="center">0.0</td>
      <td align="center">0.3</td>
      <td align="center">0.00</td>
      <td align="center">36.9</td>
      <td align="center">0.0</td>
      <td align="center">0.5</td>
      <td align="center">0.00</td>
      <td align="center">28.0</td>
      <td align="center">0.0</td>
      <td align="center">0.5</td>
      <td align="center">0.00</td>
      <td align="center">0.8</td>
      <td align="center">0.0</td>
      <td align="center">0.0</td>
      <td align="center">0.00</td>
      <td align="center">82.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/alibaba.png" width="14" height="14" alt="Alibaba">&#8288;&nbsp;Ovis2.6&#8209;30B&#8209;A3B</sub></td>
      <td align="center">✓</td>
      <td align="center">2.5</td>
      <td align="center">11.3</td>
      <td align="center">0.11</td>
      <td align="center">60.8</td>
      <td align="center">0.1</td>
      <td align="center">2.0</td>
      <td align="center">0.02</td>
      <td align="center">89.8</td>
      <td align="center">0.7</td>
      <td align="center">7.5</td>
      <td align="center">0.06</td>
      <td align="center">13.5</td>
      <td align="center">6.8</td>
      <td align="center">24.5</td>
      <td align="center">0.25</td>
      <td align="center">79.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/glmv.png" width="14" height="14" alt="GLM">&#8288;&nbsp;GLM&#8209;4.5V&nbsp;108B</sub></td>
      <td align="center">✓</td>
      <td align="center">1.8</td>
      <td align="center">6.7</td>
      <td align="center">0.06</td>
      <td align="center">69.0</td>
      <td align="center">0.1</td>
      <td align="center">4.2</td>
      <td align="center">0.04</td>
      <td align="center"><strong>100</strong></td>
      <td align="center">2.0</td>
      <td align="center">6.5</td>
      <td align="center">0.05</td>
      <td align="center">15.5</td>
      <td align="center">3.3</td>
      <td align="center">9.2</td>
      <td align="center">0.10</td>
      <td align="center">91.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/kimi.png" width="14" height="14" alt="Kimi">&#8288;&nbsp;Kimi&nbsp;K2.5</sub></td>
      <td align="center"></td>
      <td align="center">6.6</td>
      <td align="center"><strong>31.9 🏆</strong></td>
      <td align="center"><strong>0.29 🏆</strong></td>
      <td align="center">95.2</td>
      <td align="center">0.1</td>
      <td align="center">11.5</td>
      <td align="center">0.06</td>
      <td align="center"><strong>100</strong></td>
      <td align="center">7.5</td>
      <td align="center">25.8</td>
      <td align="center">0.19</td>
      <td align="center">90.0</td>
      <td align="center">12.5</td>
      <td align="center"><strong>58.5</strong></td>
      <td align="center"><strong>0.60</strong></td>
      <td align="center">95.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/kimi.png" width="14" height="14" alt="Kimi">&#8288;&nbsp;Kimi&nbsp;K2.5</sub></td>
      <td align="center">✓</td>
      <td align="center">2.4</td>
      <td align="center">24.2</td>
      <td align="center">0.28</td>
      <td align="center">93.0</td>
      <td align="center">0.0</td>
      <td align="center">10.2</td>
      <td align="center"><strong>0.07</strong></td>
      <td align="center">99.8</td>
      <td align="center">1.2</td>
      <td align="center">17.5</td>
      <td align="center">0.20</td>
      <td align="center">85.8</td>
      <td align="center">6.0</td>
      <td align="center">44.8</td>
      <td align="center">0.57</td>
      <td align="center">93.5</td>
    </tr>
    <tr><td colspan="18" align="left"><em><strong>闭源模型</strong></em></td></tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/openai.png" width="14" height="14" alt="OpenAI">&#8288;&nbsp;GPT&#8209;4o</sub></td>
      <td align="center"></td>
      <td align="center">0.1</td>
      <td align="center">2.0</td>
      <td align="center">0.03</td>
      <td align="center">77.4</td>
      <td align="center">0.0</td>
      <td align="center">0.5</td>
      <td align="center">0.01</td>
      <td align="center">96.5</td>
      <td align="center">0.0</td>
      <td align="center">1.0</td>
      <td align="center">0.02</td>
      <td align="center">46.8</td>
      <td align="center">0.3</td>
      <td align="center">4.5</td>
      <td align="center">0.06</td>
      <td align="center">89.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/openai.png" width="14" height="14" alt="OpenAI">&#8288;&nbsp;GPT&#8209;5</sub></td>
      <td align="center"></td>
      <td align="center">0.5</td>
      <td align="center">4.2</td>
      <td align="center">0.06</td>
      <td align="center">85.4</td>
      <td align="center">0.0</td>
      <td align="center">4.0</td>
      <td align="center">0.01</td>
      <td align="center">98.2</td>
      <td align="center">0.0</td>
      <td align="center">4.0</td>
      <td align="center">0.04</td>
      <td align="center">60.5</td>
      <td align="center">1.6</td>
      <td align="center">4.5</td>
      <td align="center">0.12</td>
      <td align="center">97.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/bytedance.png" width="14" height="14" alt="ByteDance">&#8288;&nbsp;Seed&nbsp;1.8</sub></td>
      <td align="center"></td>
      <td align="center">11.9</td>
      <td align="center">23.3</td>
      <td align="center">0.21</td>
      <td align="center">93.0</td>
      <td align="center">0.4</td>
      <td align="center">9.2</td>
      <td align="center">0.04</td>
      <td align="center">99.5</td>
      <td align="center">9.4</td>
      <td align="center">15.8</td>
      <td align="center">0.17</td>
      <td align="center">80.5</td>
      <td align="center">26.7</td>
      <td align="center">45.0</td>
      <td align="center">0.42</td>
      <td align="center">99.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/bytedance.png" width="14" height="14" alt="ByteDance">&#8288;&nbsp;Seed&nbsp;1.8</sub></td>
      <td align="center">✓</td>
      <td align="center">9.8</td>
      <td align="center">19.9</td>
      <td align="center">0.22</td>
      <td align="center"><strong>95.7 🏆</strong></td>
      <td align="center">0.4</td>
      <td align="center">8.8</td>
      <td align="center">0.05</td>
      <td align="center">99.5</td>
      <td align="center">5.8</td>
      <td align="center">14.8</td>
      <td align="center">0.18</td>
      <td align="center">90.0</td>
      <td align="center">23.3</td>
      <td align="center">36.2</td>
      <td align="center">0.43</td>
      <td align="center">97.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/bytedance.png" width="14" height="14" alt="ByteDance">&#8288;&nbsp;Seed&nbsp;2.0&nbsp;Pro</sub></td>
      <td align="center"></td>
      <td align="center"><strong>21.1 🏆</strong></td>
      <td align="center">27.7</td>
      <td align="center">0.23</td>
      <td align="center">95.2</td>
      <td align="center"><strong>3.0</strong></td>
      <td align="center">11.0</td>
      <td align="center">0.04</td>
      <td align="center">99.5</td>
      <td align="center"><strong>19.9</strong></td>
      <td align="center"><strong>30.8</strong></td>
      <td align="center">0.22</td>
      <td align="center"><strong>92.2</strong></td>
      <td align="center"><strong>40.7</strong></td>
      <td align="center">41.5</td>
      <td align="center">0.43</td>
      <td align="center">93.8</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/bytedance.png" width="14" height="14" alt="ByteDance">&#8288;&nbsp;Seed&nbsp;2.0&nbsp;Pro</sub></td>
      <td align="center">✓</td>
      <td align="center">19.8</td>
      <td align="center">24.9</td>
      <td align="center">0.27</td>
      <td align="center">95.5</td>
      <td align="center">2.4</td>
      <td align="center">11.2</td>
      <td align="center">0.05</td>
      <td align="center">99.8</td>
      <td align="center">17.8</td>
      <td align="center">26.0</td>
      <td align="center"><strong>0.26</strong></td>
      <td align="center"><strong>92.2</strong></td>
      <td align="center">39.1</td>
      <td align="center">37.5</td>
      <td align="center">0.49</td>
      <td align="center">94.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/xiaomimimo.png" width="14" height="14" alt="Xiaomi">&#8288;&nbsp;MiMo&#8209;V2&#8209;Omni</sub></td>
      <td align="center">✓</td>
      <td align="center">0.6</td>
      <td align="center">8.1</td>
      <td align="center">0.09</td>
      <td align="center">83.7</td>
      <td align="center">0.0</td>
      <td align="center">6.5</td>
      <td align="center">0.05</td>
      <td align="center">99.5</td>
      <td align="center">0.2</td>
      <td align="center">8.0</td>
      <td align="center">0.07</td>
      <td align="center">58.5</td>
      <td align="center">1.5</td>
      <td align="center">9.8</td>
      <td align="center">0.15</td>
      <td align="center">93.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/gemini.png" width="14" height="14" alt="Gemini">&#8288;&nbsp;Gemini&nbsp;2.5&nbsp;Pro</sub></td>
      <td align="center">✓</td>
      <td align="center">1.0</td>
      <td align="center">7.8</td>
      <td align="center">0.09</td>
      <td align="center">83.4</td>
      <td align="center">0.0</td>
      <td align="center">5.8</td>
      <td align="center">0.05</td>
      <td align="center">99.5</td>
      <td align="center">0.2</td>
      <td align="center">7.0</td>
      <td align="center">0.06</td>
      <td align="center">80.5</td>
      <td align="center">2.8</td>
      <td align="center">10.8</td>
      <td align="center">0.14</td>
      <td align="center">70.2</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/gemini.png" width="14" height="14" alt="Gemini">&#8288;&nbsp;Gemini&nbsp;3.1&nbsp;Pro</sub></td>
      <td align="center">✓</td>
      <td align="center">3.4</td>
      <td align="center">22.9</td>
      <td align="center">0.18</td>
      <td align="center">92.4</td>
      <td align="center">0.0</td>
      <td align="center"><strong>14.0</strong></td>
      <td align="center">0.06</td>
      <td align="center">99.5</td>
      <td align="center">2.5</td>
      <td align="center">22.5</td>
      <td align="center">0.18</td>
      <td align="center">84.5</td>
      <td align="center">7.8</td>
      <td align="center">32.2</td>
      <td align="center">0.32</td>
      <td align="center">93.2</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/claude.png" width="14" height="14" alt="Claude">&#8288;&nbsp;Claude&nbsp;Opus&nbsp;4.7</sub></td>
      <td align="center">✓</td>
      <td align="center">0.5</td>
      <td align="center">11.9</td>
      <td align="center">0.10</td>
      <td align="center">89.3</td>
      <td align="center">0.0</td>
      <td align="center">4.8</td>
      <td align="center">0.04</td>
      <td align="center">93.8</td>
      <td align="center">0.1</td>
      <td align="center">9.5</td>
      <td align="center">0.05</td>
      <td align="center">80.5</td>
      <td align="center">1.4</td>
      <td align="center">21.5</td>
      <td align="center">0.21</td>
      <td align="center">93.8</td>
    </tr>
  </tbody>
</table>

</details>

</details>

> **甲** = 甲骨文, **金** = 金文, **篆** = 篆书。**加粗** = 最佳。

### 成熟书体排行榜

<p align="center">
  <img src="assets/leaderboard_mature.svg" width="100%" alt="成熟书体排行榜">
</p>

<details>
<summary><strong>查看各书体详细结果</strong></summary>

<h4>Clerical Script · 隶书</h4>
<p align="center">
  <img src="assets/leaderboard_clerical.svg" width="100%" alt="Clerical Script · 隶书">
</p>

<h4>Regular Script · 楷书</h4>
<p align="center">
  <img src="assets/leaderboard_regular.svg" width="100%" alt="Regular Script · 楷书">
</p>

<h4>Running Script · 行书</h4>
<p align="center">
  <img src="assets/leaderboard_running.svg" width="100%" alt="Running Script · 行书">
</p>

<h4>Cursive Script · 草书</h4>
<p align="center">
  <img src="assets/leaderboard_cursive.svg" width="100%" alt="Cursive Script · 草书">
</p>

<details>
<summary><strong>查看原始 HTML 表格</strong></summary>

<table>
  <thead>
    <tr>
      <th width="210" rowspan="2" align="left">模型</th>
      <th rowspan="2" align="center">Think</th>
      <th colspan="2" align="center">平均</th>
      <th colspan="2" align="center">隶书</th>
      <th colspan="2" align="center">楷书</th>
      <th colspan="2" align="center">行书</th>
      <th colspan="2" align="center">草书</th>
    </tr>
    <tr>
      <th align="center">Pars.</th>
      <th align="center">Class.</th>
      <th align="center">Pars.</th>
      <th align="center">Class.</th>
      <th align="center">Pars.</th>
      <th align="center">Class.</th>
      <th align="center">Pars.</th>
      <th align="center">Class.</th>
      <th align="center">Pars.</th>
      <th align="center">Class.</th>
    </tr>
  </thead>
  <tbody>
    <tr><td colspan="12" align="left"><em><strong>开源模型</strong></em></td></tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/intern.png" width="14" height="14" alt="InternVL">&#8288;&nbsp;InternVL3.5&#8209;8B</sub></td>
      <td align="center"></td>
      <td align="center">0.40</td>
      <td align="center">39.8</td>
      <td align="center">0.41</td>
      <td align="center">1.8</td>
      <td align="center">0.51</td>
      <td align="center">69.4</td>
      <td align="center">0.38</td>
      <td align="center">52.9</td>
      <td align="center">0.30</td>
      <td align="center">35.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/intern.png" width="14" height="14" alt="InternVL">&#8288;&nbsp;InternVL3.5&#8209;A28B</sub></td>
      <td align="center"></td>
      <td align="center">0.56</td>
      <td align="center">63.1</td>
      <td align="center">0.54</td>
      <td align="center">28.5</td>
      <td align="center">0.69</td>
      <td align="center">85.5</td>
      <td align="center">0.56</td>
      <td align="center">63.3</td>
      <td align="center">0.46</td>
      <td align="center">75.2</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen2.5&#8209;VL&#8209;7B</sub></td>
      <td align="center"></td>
      <td align="center">0.45</td>
      <td align="center">38.0</td>
      <td align="center">0.54</td>
      <td align="center">8.0</td>
      <td align="center">0.62</td>
      <td align="center">17.0</td>
      <td align="center">0.42</td>
      <td align="center">36.4</td>
      <td align="center">0.21</td>
      <td align="center">90.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen2.5&#8209;VL&#8209;72B</sub></td>
      <td align="center"></td>
      <td align="center">0.49</td>
      <td align="center">63.0</td>
      <td align="center">0.59</td>
      <td align="center">18.0</td>
      <td align="center">0.66</td>
      <td align="center">91.5</td>
      <td align="center">0.46</td>
      <td align="center">56.6</td>
      <td align="center">0.26</td>
      <td align="center">86.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3&#8209;VL&#8209;2B</sub></td>
      <td align="center"></td>
      <td align="center">0.56</td>
      <td align="center">37.0</td>
      <td align="center">0.61</td>
      <td align="center">5.5</td>
      <td align="center">0.71</td>
      <td align="center">11.8</td>
      <td align="center">0.50</td>
      <td align="center">37.9</td>
      <td align="center">0.42</td>
      <td align="center">93.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3&#8209;VL&#8209;8B</sub></td>
      <td align="center"></td>
      <td align="center">0.66</td>
      <td align="center">67.5</td>
      <td align="center">0.69</td>
      <td align="center">32.5</td>
      <td align="center">0.77</td>
      <td align="center"><strong>97.2</strong></td>
      <td align="center">0.64</td>
      <td align="center">59.1</td>
      <td align="center">0.56</td>
      <td align="center">81.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3&#8209;VL&#8209;8B</sub></td>
      <td align="center">✓</td>
      <td align="center">0.50</td>
      <td align="center">50.1</td>
      <td align="center">0.52</td>
      <td align="center">11.2</td>
      <td align="center">0.64</td>
      <td align="center">79.7</td>
      <td align="center">0.51</td>
      <td align="center">53.4</td>
      <td align="center">0.32</td>
      <td align="center">56.2</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3&#8209;VL&#8209;A22B</sub></td>
      <td align="center"></td>
      <td align="center">0.67</td>
      <td align="center">70.6</td>
      <td align="center">0.69</td>
      <td align="center">36.5</td>
      <td align="center">0.73</td>
      <td align="center">95.5</td>
      <td align="center">0.66</td>
      <td align="center">68.3</td>
      <td align="center">0.59</td>
      <td align="center">82.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3&#8209;VL&#8209;A22B</sub></td>
      <td align="center">✓</td>
      <td align="center">0.65</td>
      <td align="center">66.2</td>
      <td align="center">0.67</td>
      <td align="center">31.0</td>
      <td align="center">0.75</td>
      <td align="center">93.5</td>
      <td align="center">0.65</td>
      <td align="center">62.3</td>
      <td align="center">0.54</td>
      <td align="center">78.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3.5&#8209;A3B</sub></td>
      <td align="center"></td>
      <td align="center">0.71</td>
      <td align="center">70.2</td>
      <td align="center">0.79</td>
      <td align="center">36.8</td>
      <td align="center">0.81</td>
      <td align="center">84.2</td>
      <td align="center">0.68</td>
      <td align="center">75.6</td>
      <td align="center">0.57</td>
      <td align="center">84.2</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/qwen.png" width="14" height="14" alt="Qwen">&#8288;&nbsp;Qwen3.5&#8209;A17B</sub></td>
      <td align="center"></td>
      <td align="center"><strong>0.74 🏆</strong></td>
      <td align="center">74.5</td>
      <td align="center"><strong>0.81</strong></td>
      <td align="center">52.0</td>
      <td align="center">0.81</td>
      <td align="center">81.3</td>
      <td align="center">0.67</td>
      <td align="center">75.3</td>
      <td align="center">0.66</td>
      <td align="center">89.4</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/gemma.png" width="14" height="14" alt="Gemma">&#8288;&nbsp;Gemma&nbsp;4&nbsp;31B&nbsp;it</sub></td>
      <td align="center"></td>
      <td align="center">0.34</td>
      <td align="center">60.3</td>
      <td align="center">0.37</td>
      <td align="center">9.6</td>
      <td align="center">0.56</td>
      <td align="center">81.9</td>
      <td align="center">0.33</td>
      <td align="center">65.0</td>
      <td align="center">0.09</td>
      <td align="center">84.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/minicpm.png" width="14" height="14" alt="MiniCPM">&#8288;&nbsp;MiniCPM&#8209;V&nbsp;4.5</sub></td>
      <td align="center">✓</td>
      <td align="center">0.40</td>
      <td align="center">49.0</td>
      <td align="center">0.45</td>
      <td align="center">2.8</td>
      <td align="center">0.61</td>
      <td align="center">87.5</td>
      <td align="center">0.38</td>
      <td align="center">56.9</td>
      <td align="center">0.15</td>
      <td align="center">48.8</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/AllenAI.png" width="14" height="14" alt="AllenAI">&#8288;&nbsp;Molmo&nbsp;7B&#8209;D&nbsp;0924</sub></td>
      <td align="center"></td>
      <td align="center">0.01</td>
      <td align="center">18.8</td>
      <td align="center">0.01</td>
      <td align="center"><strong>70.8</strong></td>
      <td align="center">0.01</td>
      <td align="center">3.0</td>
      <td align="center">0.01</td>
      <td align="center">0.7</td>
      <td align="center">0.01</td>
      <td align="center">0.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/AllenAI.png" width="14" height="14" alt="AllenAI">&#8288;&nbsp;Molmo&nbsp;72B&nbsp;0924</sub></td>
      <td align="center"></td>
      <td align="center">0.00</td>
      <td align="center">9.8</td>
      <td align="center">0.00</td>
      <td align="center">6.8</td>
      <td align="center">0.01</td>
      <td align="center">16.5</td>
      <td align="center">0.01</td>
      <td align="center">3.2</td>
      <td align="center">0.00</td>
      <td align="center">12.8</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/alibaba.png" width="14" height="14" alt="Alibaba">&#8288;&nbsp;Ovis2.6&#8209;30B&#8209;A3B</sub></td>
      <td align="center">✓</td>
      <td align="center">0.54</td>
      <td align="center">42.6</td>
      <td align="center">0.54</td>
      <td align="center">8.5</td>
      <td align="center">0.63</td>
      <td align="center">77.9</td>
      <td align="center">0.57</td>
      <td align="center">71.6</td>
      <td align="center">0.42</td>
      <td align="center">12.2</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/glmv.png" width="14" height="14" alt="GLM">&#8288;&nbsp;GLM&#8209;4.5V&nbsp;108B</sub></td>
      <td align="center">✓</td>
      <td align="center">0.43</td>
      <td align="center">60.2</td>
      <td align="center">0.45</td>
      <td align="center">11.5</td>
      <td align="center">0.61</td>
      <td align="center">84.5</td>
      <td align="center">0.44</td>
      <td align="center">63.3</td>
      <td align="center">0.23</td>
      <td align="center">81.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/kimi.png" width="14" height="14" alt="Kimi">&#8288;&nbsp;Kimi&nbsp;K2.5</sub></td>
      <td align="center"></td>
      <td align="center">0.72</td>
      <td align="center"><strong>78.1 🏆</strong></td>
      <td align="center">0.73</td>
      <td align="center">70.2</td>
      <td align="center">0.78</td>
      <td align="center">78.2</td>
      <td align="center">0.72</td>
      <td align="center">77.8</td>
      <td align="center">0.66</td>
      <td align="center">86.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/kimi.png" width="14" height="14" alt="Kimi">&#8288;&nbsp;Kimi&nbsp;K2.5</sub></td>
      <td align="center">✓</td>
      <td align="center">0.70</td>
      <td align="center">75.1</td>
      <td align="center">0.75</td>
      <td align="center">68.5</td>
      <td align="center">0.78</td>
      <td align="center">81.7</td>
      <td align="center">0.60</td>
      <td align="center">65.3</td>
      <td align="center"><strong>0.66</strong></td>
      <td align="center">84.8</td>
    </tr>
    <tr><td colspan="12" align="left"><em><strong>闭源模型</strong></em></td></tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/openai.png" width="14" height="14" alt="OpenAI">&#8288;&nbsp;GPT&#8209;4o</sub></td>
      <td align="center"></td>
      <td align="center">0.29</td>
      <td align="center">59.9</td>
      <td align="center">0.35</td>
      <td align="center">20.5</td>
      <td align="center">0.47</td>
      <td align="center">83.0</td>
      <td align="center">0.24</td>
      <td align="center">55.6</td>
      <td align="center">0.12</td>
      <td align="center">80.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/openai.png" width="14" height="14" alt="OpenAI">&#8288;&nbsp;GPT&#8209;5</sub></td>
      <td align="center"></td>
      <td align="center">0.37</td>
      <td align="center">61.2</td>
      <td align="center">0.50</td>
      <td align="center">36.2</td>
      <td align="center">0.57</td>
      <td align="center">59.6</td>
      <td align="center">0.21</td>
      <td align="center"><strong>78.1</strong></td>
      <td align="center">0.18</td>
      <td align="center">71.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/bytedance.png" width="14" height="14" alt="ByteDance">&#8288;&nbsp;Seed&nbsp;1.8</sub></td>
      <td align="center"></td>
      <td align="center">0.69</td>
      <td align="center">73.1</td>
      <td align="center">0.68</td>
      <td align="center">45.5</td>
      <td align="center">0.79</td>
      <td align="center">92.7</td>
      <td align="center">0.69</td>
      <td align="center">71.8</td>
      <td align="center">0.61</td>
      <td align="center">82.5</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/bytedance.png" width="14" height="14" alt="ByteDance">&#8288;&nbsp;Seed&nbsp;1.8</sub></td>
      <td align="center">✓</td>
      <td align="center">0.66</td>
      <td align="center">72.8</td>
      <td align="center">0.69</td>
      <td align="center">48.0</td>
      <td align="center">0.78</td>
      <td align="center">89.2</td>
      <td align="center">0.57</td>
      <td align="center">73.3</td>
      <td align="center">0.60</td>
      <td align="center">80.8</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/bytedance.png" width="14" height="14" alt="ByteDance">&#8288;&nbsp;Seed&nbsp;2.0&nbsp;Pro</sub></td>
      <td align="center"></td>
      <td align="center">0.72</td>
      <td align="center"><strong>78.1 🏆</strong></td>
      <td align="center">0.75</td>
      <td align="center">60.8</td>
      <td align="center">0.81</td>
      <td align="center">82.0</td>
      <td align="center"><strong>0.73</strong></td>
      <td align="center">77.6</td>
      <td align="center">0.62</td>
      <td align="center">92.2</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/bytedance.png" width="14" height="14" alt="ByteDance">&#8288;&nbsp;Seed&nbsp;2.0&nbsp;Pro</sub></td>
      <td align="center">✓</td>
      <td align="center">0.72</td>
      <td align="center">76.8</td>
      <td align="center">0.76</td>
      <td align="center">61.8</td>
      <td align="center">0.80</td>
      <td align="center">82.0</td>
      <td align="center">0.65</td>
      <td align="center">74.3</td>
      <td align="center">0.66</td>
      <td align="center">89.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/xiaomimimo.png" width="14" height="14" alt="Xiaomi">&#8288;&nbsp;MiMo&#8209;V2&#8209;Omni</sub></td>
      <td align="center">✓</td>
      <td align="center">0.56</td>
      <td align="center">64.6</td>
      <td align="center">0.62</td>
      <td align="center">40.0</td>
      <td align="center">0.71</td>
      <td align="center">80.7</td>
      <td align="center">0.58</td>
      <td align="center">73.3</td>
      <td align="center">0.36</td>
      <td align="center">64.2</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/gemini.png" width="14" height="14" alt="Gemini">&#8288;&nbsp;Gemini&nbsp;2.5&nbsp;Pro</sub></td>
      <td align="center">✓</td>
      <td align="center">0.53</td>
      <td align="center">56.8</td>
      <td align="center">0.67</td>
      <td align="center">33.2</td>
      <td align="center">0.72</td>
      <td align="center">39.6</td>
      <td align="center">0.49</td>
      <td align="center">59.4</td>
      <td align="center">0.23</td>
      <td align="center">95.0</td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/gemini.png" width="14" height="14" alt="Gemini">&#8288;&nbsp;Gemini&nbsp;3.1&nbsp;Pro</sub></td>
      <td align="center">✓</td>
      <td align="center">0.70</td>
      <td align="center">72.6</td>
      <td align="center">0.80</td>
      <td align="center">61.0</td>
      <td align="center"><strong>0.83</strong></td>
      <td align="center">62.7</td>
      <td align="center">0.66</td>
      <td align="center">71.1</td>
      <td align="center">0.52</td>
      <td align="center"><strong>95.8</strong></td>
    </tr>
    <tr>
      <td width="210" align="left"><sub><img src="https://arxiv.org/html/2605.11960v2/figures/logo/org/claude.png" width="14" height="14" alt="Claude">&#8288;&nbsp;Claude&nbsp;Opus&nbsp;4.7</sub></td>
      <td align="center">✓</td>
      <td align="center">0.49</td>
      <td align="center">66.8</td>
      <td align="center">0.53</td>
      <td align="center">50.2</td>
      <td align="center">0.63</td>
      <td align="center">74.4</td>
      <td align="center">0.44</td>
      <td align="center">56.6</td>
      <td align="center">0.38</td>
      <td align="center">86.0</td>
    </tr>
  </tbody>
</table>

</details>

</details>

> **隶** = 隶书, **楷** = 楷书, **行** = 行书, **草** = 草书。**加粗** = 最佳。

## 快速开始

### 1. 安装

```bash
git clone https://github.com/VirtualLUOUCAS/Chronicles-OCR.git
cd Chronicles-OCR
pip install -r requirements.txt
```

### 2. 下载数据

从 [🤗](https://huggingface.co/datasets/VirtualLUO/Chronicles-OCR) 或 [🤖](https://modelscope.cn/datasets/VirtualLUO/Chronicles-OCR) 下载数据并放置在 `data/` 目录下：

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

### 3. 推理

```bash
# OpenAI 兼容 API
python infer.py --api_type openai_compat \
    --model_name Qwen2.5-VL-7B-Instruct \
    --base_url http://127.0.0.1:8000/v1 \
    --api_key EMPTY --max_workers 64

# 本地 vLLM
python infer.py --api_type local_vllm \
    --model_path /path/to/model \
    --tensor_parallel_size 1 --max_model_len 32768
```

### 4. 评测（基于规则）

```bash
python judge.py                    # 评测所有模型
python judge.py --models model_a   # 评测指定模型
```

### 5. 汇总报告

```bash
python summarize.py
# → judge_results/results_analysis.xlsx
```

## 引用

```bibtex
@article{li2026chronicles,
  title   = {{Chronicles-OCR}: A Cross-Temporal Perception Benchmark for the Evolutionary Trajectory of Chinese Characters},
  author  = {Gengluo Li and Shangping Peng and Xingyu Wan and Chengquan Zhang and Hao Feng and Xin Xu and Pian Wu and Bang Li and Zengmao Ding and Yongge Liu and Yipei Ye and Yang Yang and Zhan Shu and Guojun Yan and Zhe Li and Can Ma and Weiping Wang and Yu Zhou and Han Hu},
  journal = {arXiv preprint arXiv:2605.11960},
  year    = {2026}
}
```

## 致谢

衷心感谢安阳师范学院甲骨文信息处理教育部重点实验室和故宫博物院在数据来源和专家标注方面的宝贵贡献。

## 许可

本基准仅供**学术研究**使用。
