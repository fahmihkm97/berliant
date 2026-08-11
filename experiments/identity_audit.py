import argparse
import re
from pathlib import Path

TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".jsonl",
    ".csv",
    ".txt",
    ".sh",
    ".bib",
}

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
}

IDENTITY_PATTERNS = {
    "username": re.compile(
        r"fahmihkm97",
        re.IGNORECASE,
    ),
    "name/path fragment": re.compile(
        r"\bfahmi\b",
        re.IGNORECASE,
    ),
    "hostname fragment": re.compile(
        r"fhmhkm",
        re.IGNORECASE,
    ),
    "home path": re.compile(
        r"/home/fahmi",
        re.IGNORECASE,
    ),
    "personal repository": re.compile(
        r"github\.com/fahmihkm97",
        re.IGNORECASE,
    ),
}


def should_scan(
    path: Path,
) -> bool:
    if any(part in IGNORE_DIRS for part in path.parts):
        return False

    return path.is_file() and path.suffix.lower() in TEXT_SUFFIXES


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
    )

    args = parser.parse_args()

    root = args.root.resolve()

    findings: list[tuple[str, Path, int, str]] = []

    for path in root.rglob("*"):
        if not should_scan(path):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(
            text.splitlines(),
            start=1,
        ):
            for label, pattern in IDENTITY_PATTERNS.items():
                if pattern.search(line):
                    findings.append(
                        (
                            label,
                            path.relative_to(root),
                            line_number,
                            line.strip(),
                        )
                    )

    print("=== Anonymous identity audit ===")

    if not findings:
        print("PASS: no configured identity markers found")
        return

    for (
        label,
        path,
        line_number,
        line,
    ) in findings:
        print(f"FOUND [{label}] {path}:{line_number}: {line}")

    raise SystemExit("IDENTITY AUDIT FAILED")


if __name__ == "__main__":
    main()
