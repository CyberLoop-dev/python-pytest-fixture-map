from __future__ import annotations
import argparse
import ast
import json
from pathlib import Path

BUILTINS = {"request", "tmp_path", "tmp_path_factory", "monkeypatch", "capsys", "capfd",
            "caplog", "cache", "pytestconfig", "record_property", "record_testsuite_property"}

def fixture_decorator(node: ast.FunctionDef | ast.AsyncFunctionDef):
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        is_fixture = (
            isinstance(target, ast.Attribute) and target.attr == "fixture"
        ) or (
            isinstance(target, ast.Name) and target.id == "fixture"
        )
        if not is_fixture:
            continue
        explicit_name = None
        scope = "function"
        autouse = False
        if isinstance(decorator, ast.Call):
            for kw in decorator.keywords:
                if kw.arg == "name" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    explicit_name = kw.value.value
                elif kw.arg == "scope" and isinstance(kw.value, ast.Constant):
                    scope = str(kw.value.value)
                elif kw.arg == "autouse" and isinstance(kw.value, ast.Constant):
                    autouse = bool(kw.value.value)
        return explicit_name or node.name, scope, autouse
    return None

def arguments(node):
    args = [a.arg for a in node.args.args]
    return [a for a in args if a not in {"self", "cls"}]

def scan(root: Path):
    fixtures, tests, warnings = {}, [], []
    for path in sorted(root.rglob("*.py")):
        if any(part in {".git", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeError, SyntaxError) as exc:
            warnings.append({"file": str(path), "error": str(exc)})
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found = fixture_decorator(node)
                if found:
                    fixture_name, scope, autouse = found
                    fixtures[fixture_name] = {
                        "file": str(path.relative_to(root)),
                        "scope": scope,
                        "autouse": autouse,
                        "dependencies": arguments(node),
                    }
                elif node.name.startswith("test_"):
                    tests.append({
                        "name": f"{path.relative_to(root)}::{node.name}",
                        "dependencies": arguments(node),
                    })
    return {"fixtures": fixtures, "tests": tests, "warnings": warnings}

def mermaid(data):
    lines = ["graph TD"]
    known = set(data["fixtures"])
    for name, item in sorted(data["fixtures"].items()):
        node = "f_" + str(abs(hash(name)))
        label = f"{name} ({item['scope']})"
        lines.append(f'  {node}["{label}"]')
        for dep in item["dependencies"]:
            if dep in known:
                lines.append(f'  {node} --> f_{abs(hash(dep))}')
    for index, test in enumerate(data["tests"]):
        node = f"t_{index}"
        lines.append(f'  {node}["{test["name"]}"]')
        for dep in test["dependencies"]:
            if dep in known:
                lines.append(f'  {node} --> f_{abs(hash(dep))}')
    return "\n".join(lines)

def main(argv=None):
    parser = argparse.ArgumentParser(description="Map pytest fixtures using AST only; project code is never imported.")
    parser.add_argument("path", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--format", choices=("mermaid", "json", "text"), default="mermaid")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.path.resolve()
    data = scan(root)
    if args.format == "json":
        output = json.dumps(data, indent=2)
    elif args.format == "text":
        lines = [f"Fixtures: {len(data['fixtures'])}", f"Tests: {len(data['tests'])}"]
        for name, item in sorted(data["fixtures"].items()):
            lines.append(f"- {name} [{item['scope']}] in {item['file']} <- {', '.join(item['dependencies']) or '(none)'}")
        output = "\n".join(lines)
    else:
        output = mermaid(data)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    if data["warnings"]:
        print(f"\nWarnings: {len(data['warnings'])} file(s) could not be parsed.", file=__import__("sys").stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
