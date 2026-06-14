import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\{\{(img_\d{2})\}\}")


def parse_args():
    parser = argparse.ArgumentParser(description="Run and validate the auto-lab workflow.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("validate", "images", "run"):
        sub = subparsers.add_parser(name)
        sub.add_argument("--workflow", required=True, help="Path to workflow.json")

    return parser.parse_args()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_workflow(path_str: str):
    path = Path(path_str).expanduser().resolve()
    workflow = load_json(path)
    workflow["_workflow_path"] = str(path)
    return workflow


def placeholder_keys(copywriting_path: Path):
    content = copywriting_path.read_text(encoding="utf-8")
    return sorted(set(PLACEHOLDER_RE.findall(content)))


def lint_prompt_config(prompt_config):
    policy = prompt_config.get("image_policy", {})
    forbidden_terms = [term.lower() for term in policy.get("forbidden_terms", [])]
    default_mode = policy.get("default_mode", "screenshot_strict")
    errors = []

    for image in prompt_config.get("images", []):
        mode = image.get("mode", default_mode)
        prompt = image.get("prompt", "")
        lower_prompt = prompt.lower()
        if mode == "screenshot_strict":
            bad_terms = [term for term in forbidden_terms if term in lower_prompt]
            if bad_terms:
                errors.append(f"{image.get('name', '<unknown>')}: forbidden terms for screenshot mode: {', '.join(bad_terms)}")
    return errors


def validate_workflow(workflow):
    output = []

    def note(message):
        output.append(message)

    requirements = Path(workflow["requirements_path"])
    template = Path(workflow["template_path"])
    output_dir = Path(workflow["output_dir"])
    copywriting_path = Path(workflow["copywriting_path"])
    prompt_config_path = Path(workflow["prompt_config_path"])
    insert_config_path = Path(workflow["insert_config_path"])
    template_manifest_path = Path(workflow["template_manifest_path"])
    docx_scripts = workflow.get("docx_scripts", {})
    fill_script = Path(docx_scripts.get("fill", ""))
    insert_script = Path(docx_scripts.get("insert", ""))
    verify_script = Path(docx_scripts.get("verify", ""))

    missing = [str(path) for path in (requirements, template, output_dir, copywriting_path, prompt_config_path, insert_config_path, template_manifest_path, fill_script, insert_script, verify_script) if not path.exists()]
    if missing:
        raise SystemExit("Missing required files:\n" + "\n".join(missing))

    prompt_config = load_json(prompt_config_path)
    insert_config = load_json(insert_config_path)

    copy_keys = placeholder_keys(copywriting_path)
    prompt_keys = [item["name"] for item in prompt_config.get("images", [])]
    insert_keys = sorted(insert_config.get("images", {}).keys())

    note(f"Placeholders in 配文.md: {len(copy_keys)}")
    note(f"Images in prompt_config.json: {len(prompt_keys)}")
    note(f"Images in insert_config.json: {len(insert_keys)}")
    note(f"Template manifest: {template_manifest_path.name}")

    if sorted(prompt_keys) != sorted(copy_keys):
        raise SystemExit("Placeholder mismatch between 配文.md and prompt_config.json")

    if insert_keys and sorted(insert_keys) != sorted(copy_keys):
        raise SystemExit("Placeholder mismatch between 配文.md and insert_config.json")

    prompt_errors = lint_prompt_config(prompt_config)
    if prompt_errors and prompt_config.get("image_policy", {}).get("fail_on_prompt_risk", True):
        raise SystemExit("Prompt policy validation failed:\n" + "\n".join(prompt_errors))

    return prompt_config, insert_config, output


def ensure_docx_scripts_customized(workflow):
    docx_scripts = workflow.get("docx_scripts", {})
    stubbed = []
    for name in ("fill", "insert", "verify"):
        script_path = Path(docx_scripts[name])
        content = script_path.read_text(encoding="utf-8")
        if "AUTO_LAB_TEMPLATE_SCRIPT_STUB = True" in content:
            stubbed.append(f"{name}: {script_path}")
    if stubbed:
        raise SystemExit(
            "Template-specific docx scripts are still stubs. Customize them for the current template before run:\n"
            + "\n".join(stubbed)
        )


def update_insert_config_from_prompts(workflow, prompt_config, insert_config):
    images_dir = Path(workflow["images_dir"])
    insert_config["target_docx"] = workflow["output_docx"]
    insert_config["images"] = {
        item["name"]: str((images_dir / f"{item['name']}.png").resolve())
        for item in prompt_config.get("images", [])
    }
    save_json(Path(workflow["insert_config_path"]), insert_config)


def run_generate_py(workflow):
    root = Path(__file__).resolve().parent
    prompt_config_path = Path(workflow["prompt_config_path"])
    command = [sys.executable, str((root / "generate_images.py").resolve()), str(prompt_config_path)]
    subprocess.run(command, check=True)


def expand_command(template, workflow):
    replacements = {
        "{template}": workflow["template_path"],
        "{requirements}": workflow["requirements_path"],
        "{output_dir}": workflow["output_dir"],
        "{output_docx}": workflow["output_docx"],
        "{copywriting}": workflow["copywriting_path"],
        "{prompt_config}": workflow["prompt_config_path"],
        "{insert_config}": workflow["insert_config_path"],
        "{images_dir}": workflow["images_dir"],
        "{fill_script}": workflow["docx_scripts"]["fill"],
        "{insert_script}": workflow["docx_scripts"]["insert"],
        "{verify_script}": workflow["docx_scripts"]["verify"],
    }
    command = template
    for key, value in replacements.items():
        command = command.replace(key, value)
    return command


def run_manifest_commands(workflow):
    commands = workflow.get("commands", {})
    for command_name in ("fill_command", "insert_command", "verify_command"):
        template = commands.get(command_name, "").strip()
        if not template:
            continue
        command = expand_command(template, workflow)
        print(f"Running {command_name}: {command}")
        subprocess.run(command, check=True, shell=True)


def main():
    args = parse_args()
    workflow = load_workflow(args.workflow)
    prompt_config, insert_config, notes = validate_workflow(workflow)

    for note in notes:
        print(note)

    if args.command == "validate":
        print("Validation passed.")
        return

    update_insert_config_from_prompts(workflow, prompt_config, insert_config)

    if args.command == "images":
        run_generate_py(workflow)
        print("Image generation finished.")
        return

    if args.command == "run":
        ensure_docx_scripts_customized(workflow)
        run_generate_py(workflow)
        run_manifest_commands(workflow)
        print("Workflow run finished.")


if __name__ == "__main__":
    main()
