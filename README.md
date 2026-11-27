<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:0f766e&height=170&section=header&text=Pytest%20Fixture%20Map&fontSize=34&fontColor=ffffff&animation=twinkling)

[![Typing](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=19&pause=1000&color=14B8A6&center=true&vCenter=true&width=650&lines=Small+tool%2C+clear+insight;Local-first+%E2%80%A2+Beginner-friendly)](https://git.io/typing-svg)

![License](https://img.shields.io/github/license/CyberLoop-dev/python-pytest-fixture-map)
![Language](https://img.shields.io/github/languages/top/CyberLoop-dev/python-pytest-fixture-map)
![Stars](https://img.shields.io/github/stars/CyberLoop-dev/python-pytest-fixture-map)
![Last commit](https://img.shields.io/github/last-commit/CyberLoop-dev/python-pytest-fixture-map)

![Project mark](assets/mark.svg)

</div>

## 📖 Overview

A static analyzer that scans Python files with `ast` and maps pytest fixture definitions to fixture dependencies and test-function parameters. It never imports or executes the inspected project.

## ✨ Features

- 🧭 Find fixture definitions in test files and conftest.py
- 🔗 Connect fixture dependencies and test-function parameters
- 🧪 Show fixture scope and autouse metadata
- 🛡️ Parse source with AST without importing project modules
- 📊 Export Mermaid, JSON, or readable text

## 🖥️ Demo

No hosted demo is claimed. Run the project locally using the steps below.

## 🚀 Quick Start

```bash
python -m pip install -e .
pytest-fixture-map ./tests
pytest-fixture-map . --format json --output fixture-map.json
```

## 🧰 Tech Stack

Python 3.10+ standard library (`ast`, `pathlib`, `json`); Mermaid-compatible output.

## 🗂️ Folder Structure

```text
python-pytest-fixture-map/
├── pytest_fixture_map.py
├── tests/test_pytest_fixture_map.py
├── assets/mark.svg
├── pyproject.toml
├── .gitignore
├── LICENSE
└── README.md
```

## 🗺️ Roadmap

- [ ] Add more edge-case examples
- [ ] Improve machine-readable output and documentation
- [ ] Expand the automated test fixtures

## 🤝 Contributing

Issues and pull requests are welcome. Keep changes focused, document behavior, and add a regression test for each bug fix.

## 📄 License

Released under the [MIT License](LICENSE).

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:0f766e,100:111827&height=110&section=footer&animation=twinkling)

</div>
