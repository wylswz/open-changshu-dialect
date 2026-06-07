---
name: changshu-dialect
description: 常熟方言语料数据集维护。Use when working on OCR digitization, dataset editing, or validation of the Changshu dialect corpus.
metadata:
  short-description: 常熟方言语料数据集
---

# 常熟方言语料数据集 (Changshu Dialect Corpus)

常熟方言的歇后語、词汇表和语法特点数据集，来源为《常熟方言词汇》（广陵书社）的 OCR 数字化。

## 项目结构

```
dataset/          # 最终数据集（Git 跟踪）
  slang.yaml      # 歇后語 616条, riddle + answer
  vocab-short.yaml      # 词汇表 497条, term + definition + section
  syntax.md       # 语法特点长文
input/            # 原始书页图片 (gitignore)
sentences/          # 歇后語书页
vocab/              # 词汇表书页
syntax/             # 语法特点书页
scripts/          # OCR 与后处理脚本（adhoc，会变动）
```

## 数据格式

### slang.yaml — 歇后語

```yaml
- riddle: 鼻头里插葱
  answer: 装象。
- riddle: 癞子做和尚
  answer: 正好。
```

按首字笔画数升序排列。

### vocab-short.yaml — 词汇表（精简版）

```yaml
- term: 板定
  definition: 一定、必定
- term: 勒笃、勒拉
  definition: 在……里
  section: 七、介词
```

按语法分类组织（介词、连词、助词、叹词等）。

### syntax.md — 语法特点

常熟方言语法特征介绍，包括叠字用法、前后缀变动、语序特点等。

## OCR 工作流

1. **原始图片** 放入 `input/<category>/` 下
2. **运行 OCR**：使用 `scripts/` 下的识别脚本，当前主力为 GPT-5.5 Vision 方案
3. **人工校对**：对照原书逐条校验，修正识别错误
4. **格式化输出**：转为 YAML/Markdown 存入 `dataset/`

### OCR 方案选择

可选的 OCR 引擎及其特点：

| 方案 | 精度 | 速度 | 成本 |
|------|------|------|------|
| VLM (GPT-5.5 等视觉大模型) | ★★★★★ | 中 | API 付费 |
| PaddleX layout_parsing | ★★★ | 慢 | 免费 |
| PaddleOCR 传统 OCR | ★★ | 快 | 免费 |

根据精度要求和预算选择合适方案。

## 注意事项

- `input/` 和 `output/` 已被 gitignore，不要提交到 GitHub（版权风险）
- 文件编号 ≠ 书页页码，需要人工确认页码映射和排序
- 最终数据需要反复对照原书校验（见 README TODO）
- 用 `uv` 管理依赖，不要用 `pip install`
