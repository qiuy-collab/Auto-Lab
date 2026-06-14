# Auto Lab

Template-preserving lab report workflow for:
- generating copywriting with image placeholders
- generating realistic screenshot-style images
- creating task-specific DOCX scripts per template
- running validation before image generation and document writes

## Structure

- `SKILL.md`: skill entrypoint
- `scripts/`: runnable workflow scripts
- `docs/prompts/`: prompt and fill rules
- `examples/`: example JSON configs
- `vendor/minimax-docx/`: vendored reference skill for OpenXML patterns

## Workflow

1. Run environment check:
   - `powershell -ExecutionPolicy Bypass -File scripts/env_check.ps1`
2. Initialize a task run directory:
   - `python scripts/init_run.py --requirements <requirements> --template <template.docx> --output-dir <output_dir> --output-docx-name <result.docx>`
3. Review generated task files:
   - `workflow.json`
   - `template_manifest.json`
   - `task_scripts/fill_template.py`
   - `task_scripts/insert_images.py`
   - `task_scripts/verify_template.py`
4. Customize the task-specific scripts for the current template.
5. Fill `配文.md`, `prompt_config.json`, and `insert_config.json`.
6. Validate:
   - `python scripts/run_workflow.py validate --workflow <workflow.json>`
7. Run:
   - `python scripts/run_workflow.py run --workflow <workflow.json>`

## Notes

- The template must be preserved. Do not use a generic filler for final document writes.
- `.env` is local-only and should never be committed.
- GitHub repository names cannot contain spaces. Use `Auto-Lab` or `AutoLab` when creating a remote repository.
