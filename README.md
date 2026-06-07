# 常熟方言 (Changshu Dialect) Dataset

常熟方言语料数据集，来源为纸质书籍的 OCR 数字化。

## 数据集内容

### `slang.yaml` — 歇后語（616 条）

两条引子式的熟语，每条包含谜面（riddle）与谜底（answer）。

```yaml
- riddle: 算盘珠
  answer: 拨一拨动一动。
- riddle: 鼻头里插葱
  answer: 装象。
```

按首字笔画数升序排列。

### `vocab.yaml` — 词汇表（497 条）

常熟方言词汇与释义，按语法分类（介词、连词、助词等）组织。

```yaml
- term: 勿牢
  definition: 难道
- term: 勒笃、勒拉
  definition: 在……里
  section: 七、介词
```

### `syntax.md` — 语法特点

常熟方言的主要语法特征介绍，包括叠字用法、语序特点等。

## 目录结构

```
├── dataset/          # 最终数据集（Git 跟踪）
│   ├── slang.yaml    # 歇后語
│   ├── vocab.yaml    # 词汇表
│   └── syntax.md     # 语法特点
├── input/            # 原始书页图片（临时，不跟踪）
│   ├── sentences/    # 歇后語书页 (1-8.jpg)
│   ├── vocab/        # 词汇表书页 (1-8.jpg)
│   └── syntax/       # 语法特点书页 (9-11.jpg)
├── output/           # 中间产物（临时，不跟踪）
├── scripts/          # OCR 与后处理脚本
│   ├── ocr_vlm.py    # GPT-5.5 Vision 批量 OCR
│   └── ...           # 其他工具脚本
└── pyproject.toml    # uv 项目配置
```

## TODO

- [ ] 反复校验 OCR 识别结果，对照原书逐条确认

## 参考文献

- 《常熟方言词汇》，广陵书社

## 数字化流程
注：本仓库工作流程需要 Agent 辅助。

1. **原始图片** → `input/` 目录，命名为 `1.jpg` ~ `N.jpg`
2. **OCR 识别** → `scripts/ocr_vlm.py` 使用 GPT-5.5 Vision 模型提取文字
3. **人工校对** → 对比 OCR 与 VLM 结果，修正识别错误
4. **格式化** → 转换为 YAML / Markdown，存入 `dataset/`
