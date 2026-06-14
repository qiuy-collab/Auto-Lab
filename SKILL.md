---
name: auto-lab
description: Portable lab-report workflow for generating copywriting, image configs, realistic screenshots, and final DOCX delivery with explicit environment checks and run manifests.
---

# auto-lab

Use this skill when the user wants to generate a lab report from a requirement document and a Word template while preserving the template structure.

This skill is the workflow wrapper around:
- `scripts/generate_images.py` for image generation
- template-specific docx scripts generated per task
- `vendor/minimax-docx/SKILL.md` as the reference skill for docx editing patterns

## What changed

This entrypoint replaces the old "read a long workflow note and remember everything" model with:
- a real skill entry file
- an explicit environment check
- an initialized run directory with fixed file names
- a workflow manifest that records paths and commands
- template analysis plus per-task docx script stubs
- prompt linting for screenshot realism before image generation

## Required order

1. Run environment check:
   - Windows PowerShell: `powershell -ExecutionPolicy Bypass -File scripts/env_check.ps1`
2. Initialize a run directory:
   - `python scripts/init_run.py --requirements <需求文档> --template <模板.docx> --output-dir <输出目录> --output-docx-name <结果文件名.docx>`
3. Read the generated files in the run directory:
   - `workflow.json`
   - `template_manifest.json`
   - `配文.md`
   - `prompt_config.json`
   - `insert_config.json`
   - `task_scripts/fill_template.py`
   - `task_scripts/insert_images.py`
   - `task_scripts/verify_template.py`
4. Analyze the current template and customize the generated docx scripts for this template only.
5. Write `配文.md`, `prompt_config.json`, and `insert_config.json`.
6. Validate the artifacts:
   - `python scripts/run_workflow.py validate --workflow <workflow.json>`
7. Generate images only after validation passes:
   - `python scripts/run_workflow.py images --workflow <workflow.json>`
8. Fill the docx and insert images through the template-specific scripts recorded in `workflow.json`:
   - `python scripts/run_workflow.py run --workflow <workflow.json>`

## Important rules

- Do not assume `AskUserQuestion` exists. If a required path is missing, ask in plain text.
- Do not write directly into the template file. Always write to the initialized output path from `workflow.json`.
- Do not use a generic docx filler as the default path. Each run must customize the generated scripts for the current template.
- Generate `配文.md` and image placeholders before generating any image.
- For screenshot-like images, do not ask the model for diagrams, arrows, annotations, callouts, posters, or explanatory text panels.
- Use `vendor/minimax-docx/SKILL.md` for docx manipulation patterns. Read that skill before implementing the current run's template-specific scripts.

## Files created by init_run.py

- `workflow.json`: authoritative run manifest
- `template_manifest.json`: snapshot of the current template structure
- `配文.md`: copywriting file with `{{img_XX}}` placeholders
- `prompt_config.json`: image config consumed by `scripts/generate_images.py`
- `insert_config.json`: image-path map for the docx insertion step
- `task_scripts/*.py`: template-specific script stubs that must be customized for the current template

## Command manifest model

`workflow.json` contains command templates for:
- `fill_command`
- `insert_command`
- `verify_command`

Supported placeholders:
- `{template}`
- `{requirements}`
- `{output_dir}`
- `{output_docx}`
- `{copywriting}`
- `{prompt_config}`
- `{insert_config}`
- `{images_dir}`
- `{fill_script}`
- `{insert_script}`
- `{verify_script}`

The workflow runner expands these placeholders and executes the commands sequentially. It refuses to run if the task-specific docx scripts are still untouched stubs.

## Examples

- `examples/prompt_config.example.json`
- `examples/insert_config.example.json`
