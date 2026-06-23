# Auto Lab

**一份需求文档 + 一个 Word 模板，自动生成排版完整的实验报告。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

---

## 它能做什么

把写实验报告里最磨人的事交给脚本，你只需要确认结果。

| 你只需要做 | Auto Lab 替你完成 |
|-----------|------------------|
| 给一份作业要求和模板 | 按模板格式填完整份报告 |
| 说清楚要配哪些图 | AI 生成终端截图 / 流程图 / ER 图 |
| 看一眼输出结果 | 自动清理格式指令、对齐图例、统一口吻 |
| 确认没问题 | 打包成 `submit.zip`，直接提交 |

不是帮你写一句话再让你改一句话——是从模板到交付，中间每一步都走完。

---

## 一个例子

以一份《大数据处理技术》课程大作业为例：

**输入**
- 1 份作业要求文档
- 1 个学校发的 Word 模板

**输出**
- 完整的 PySpark 代码和分析结果
- 12 张终端/IDE 截图（AI 生成，不是截图工具抠的）
- 排版完好的 Word 报告，封面、目录、正文、图例全部到位
- `submit/` 文件夹 + `submit.zip`，一键交作业

---

## 怎么开始

```bash
# 克隆仓库
git clone https://github.com/qiuy-collab/Auto-Lab.skill.git
cd Auto-Lab.skill

# 安装依赖
pip install requests python-docx Pillow

# 初始化一次运行
python scripts/init_run.py \
  --requirements 作业要求.txt \
  --template 实验报告模板.docx \
  --output-dir ./run01 \
  --output-docx-name 实验报告.docx

# 之后 AI 会自动走完后续流程——你只需要在两个关键节点看一眼确认
```

> 详细用法见 [SKILL.md](SKILL.md)。

---

## 项目结构

```
Auto-Lab.skill/
├── SKILL.md                   # 执行指南
├── README.md                  # 本文件
├── .env.example               # API 配置（可选，AI 截图需要）
├── scripts/                   # 核心脚本
│   ├── init_run.py            # 初始化运行目录
│   ├── run_workflow.py        # 工作流引擎
│   ├── generate_images.py     # AI 截图生成
│   └── package_submission.py  # 打包交付
├── examples/                  # 完整示例
│   └── big-data-processing-report/
├── docs/                      # 规则文档 & GitHub Pages
└── vendor/                    # 附属能力
    ├── minimax-docx/
    ├── frontend-design/
    └── webapp-testing/
```

---

## 许可证

MIT License © [qiuy-collab](https://github.com/qiuy-collab)

---

**Auto Lab** — 把时间花在思考上，把排版交给工具。
