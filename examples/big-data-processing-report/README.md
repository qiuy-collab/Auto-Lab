# Example: Big Data Processing Report

This is a complete example of an auto-lab run for a university course assignment.

## Input

- **Requirement**: `《大数据处理技术》.docx` — Course assignment document

## Output

- **Final DOCX**: `大数据处理技术课程大作业报告_AI版.docx`
- **Submit package**: `submit-nieshengyu.zip` containing:
  - `大数据处理技术课程大作业报告.docx` — Filled report
  - `code/` — Python scripts (generate_raw_data.py, clean_data.py, pyspark_analysis.py, visualize_data.py)
  - `data/` — Raw and cleaned CSV datasets
  - `output/` — Analysis results (CSV, JSON, PNG charts)

## Configuration Files

| File | Purpose |
|------|---------|
| `requirement_analysis.json` | Semantic decisions from requirement reading |
| `requirement_checklist.json` | Execution flags and figure placement plan |
| `prompt_config.json` | AI image generation prompts (12 images) |
| `insert_config.json` | Image insertion positions in DOCX |
| `workflow.json` | Complete workflow state |
| `template_manifest.json` | DOCX template structure analysis |
| `pre_task_plan.json` | Pre-task completion record |
| `submission_package.json` | Final delivery manifest |

## Routes Used

- `ai_simulated`: 12 AI-generated terminal/IDE screenshots
- `diagram_assets`: None (no diagrams needed for this assignment)

## Key Decisions

1. Pre-task required: Yes — generate sample data, write PySpark analysis code
2. Image route: AI-simulated for all terminal/IDE screenshots
3. Voice: Student perspective (not agent/tool perspective)
4. Template: Preserved structure, removed placeholder text
