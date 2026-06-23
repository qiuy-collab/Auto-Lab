<div align="center">

# autolab.skill

**一个用于实验报告、课程设计报告和作业文档交付的自动化 skill。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

</div>

---

## 实验报告排版复杂？

还在为学校发的 Word 模板头疼？  
还在一张张整理运行截图、流程图、ER 图？  
还在反复调整格式、目录、图注和提交文件？  
课程设计、大作业、实验报告、毕设材料不想再手动填一遍？

`autolab.skill` 想解决的就是这些重复工作。

它会把：

```text
作业要求 → 需求分析 → 报告规划 → 配图 → Word 填写 → 检查 → 打包
```

这一整条流程串起来，让 AI Agent 按固定步骤完成报告交付。

---

## 它能做什么

`autolab.skill` 主要用于自动化处理课程报告和实验文档，包括：

- 数据分析实验报告
- Linux / 操作系统实操报告
- Python / Java / Web 开发报告
- 管理系统开发课程设计
- 数据库设计与 ER 图整理
- 流程图、架构图、运行截图等材料生成
- Word 模板填充、格式清理和图文排版
- `submit/` 文件夹与 `submit.zip` 提交包整理

它不是只生成正文，而是尽量把报告从准备到交付的流程跑完整。

---

## Quick Start

把下面这段提示词发给你的 AI Agent：

```text
请读取并初始化这个 skill：

https://github.com/qiuy-collab/Auto-Lab.skill

这是一个用于实验报告、课程设计报告和 Word 模板填写的自动化 skill。

请先完成初始化：

1. 克隆仓库。
2. 阅读 SKILL.md。
3. 根据 SKILL.md 检查运行环境。
4. 自动安装基础依赖。
5. 检查 vendor skills 是否完整。
6. 运行环境检查脚本。
7. 如果缺少必要配置，请告诉我需要补充什么文件或参数。

注意：
- 现在只做初始化和环境准备。
- 不要开始生成报告。
- 不要修改原始 Word 模板。
- 不要跳过 SKILL.md 里的流程规则。
```

---

## 运行效果展示

下面是一份《大数据处理技术》课程大作业的示例输出。

### 输入

| 类型 | 内容 |
|---|---|
| 作业要求 | 《大数据处理技术》课程大作业 |
| 报告模板 | 学校发的 Word 实验报告模板 |
| 实验内容 | PySpark 数据处理、清洗、分析和可视化 |
| 输出目标 | 代码、数据、图表、截图、报告 DOCX、提交包 |

### 生成流程

```mermaid
flowchart LR
    A[作业要求] --> B[需求分析]
    B --> C[报告规划]
    C --> D[代码与数据处理]
    D --> E[截图与图表]
    E --> F[Word 报告填充]
    F --> G[submit 文件夹]
    G --> H[submit.zip]
```

### 输出

| 输出内容 | 说明 |
|---|---|
| `大数据处理技术课程大作业报告.docx` | 按模板填好的完整课程报告 |
| `code/` | 数据生成、清洗、分析、可视化脚本 |
| `data/` | 原始数据和清洗后的数据 |
| `output/` | CSV 分析结果和图表输出 |
| 12 张实验截图 | Ubuntu + Hadoop + Hive + Spark 风格的终端 / IDE 截图 |
| `submit/` | 可直接检查的提交文件夹 |
| `submit.zip` | 最终提交压缩包 |

### 示例目录

```text
examples/big-data-processing-report/
├── 需求/
│   └── 《大数据处理技术》.docx
├── 交付/
│   ├── 大数据处理技术课程大作业报告.docx
│   ├── code/
│   ├── data/
│   └── output/
└── 效果图/
```

---

## Project Structure

```text
Auto-Lab.skill/
├── SKILL.md                   # skill 执行指南
├── README.md                  # 项目说明
├── .env.example               # AI 截图接口配置示例
├── scripts/                   # 核心脚本
│   ├── init_run.py            # 初始化运行目录
│   ├── run_workflow.py        # 工作流验证与执行
│   ├── generate_images.py     # AI 截图生成
│   └── package_submission.py  # 提交文件打包
├── examples/                  # 示例任务
│   └── big-data-processing-report/
├── docs/                      # 规则文档
└── vendor/                    # 配套 skill
    ├── minimax-docx/
    ├── baseline-ui/
    ├── frontend-design/
    └── webapp-testing/
```

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=qiuy-collab/Auto-Lab.skill&type=Date)](https://www.star-history.com/#qiuy-collab/Auto-Lab.skill&Date)

---

## License

MIT License © [qiuy-collab](https://github.com/qiuy-collab)
