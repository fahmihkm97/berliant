import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
SECTIONS = PAPER / "sections"
ICST = PAPER / "icst"
GENERATED = ICST / "generated"
FIGURES = ICST / "figures"

SECTION_FILES = (
    "00_introduction.md",
    "01a_related_work.md",
    "01_research_questions.md",
    "02_methodology.md",
    "03_experimental_setup.md",
    "04_results.md",
    "05_discussion.md",
    "06_limitations_and_threats.md",
    "07_conclusion.md",
)

FIGURE_NAMES = (
    "figure_1_recovery_comparison.pdf",
    "figure_2_execution_comparison.pdf",
    "figure_3_scaling.pdf",
    "figure_4_scaling_reduction.pdf",
    "figure_5_holdout_recovery.pdf",
)


def normalize_markdown(
    text: str,
) -> str:
    # Pandoc 2.9 treats \[ and \] as escaped brackets.
    text = re.sub(
        r"(?m)^[ \t]*\\\[[ \t]*$",
        "$$",
        text,
    )

    text = re.sub(
        r"(?m)^[ \t]*\\\][ \t]*$",
        "$$",
        text,
    )

    # Normalize inline LaTeX math delimiters when present.
    text = re.sub(
        r"\\\((.+?)\\\)",
        r"$\1$",
        text,
    )

    return text


def convert(
    source: Path,
    output: Path,
    *,
    abstract: bool = False,
) -> str:
    markdown = source.read_text(
        encoding="utf-8",
    )

    if abstract:
        markdown = re.sub(
            r"\A# Abstract\s*\n+",
            "",
            markdown,
            count=1,
        )

    markdown = normalize_markdown(markdown)

    command = [
        "pandoc",
        "--from=markdown-auto_identifiers+tex_math_dollars+tex_math_single_backslash+raw_tex",
        "--to=latex",
        "--natbib",
        "--wrap=none",
    ]

    result = subprocess.run(
        command,
        input=markdown,
        text=True,
        capture_output=True,
        check=True,
    )

    latex = result.stdout

    # IEEEtran uses numeric \cite rather than natbib \citep.
    latex = latex.replace(
        r"\citep{",
        r"\cite{",
    )

    latex = latex.replace(
        r"\citet{",
        r"\cite{",
    )

    output.write_text(
        latex,
        encoding="utf-8",
    )

    return latex


if GENERATED.exists():
    shutil.rmtree(GENERATED)

GENERATED.mkdir(
    parents=True,
    exist_ok=True,
)

FIGURES.mkdir(
    parents=True,
    exist_ok=True,
)

abstract_tex = convert(
    SECTIONS / "08_abstract.md",
    GENERATED / "08_abstract.tex",
    abstract=True,
)

all_latex = [abstract_tex]

for filename in SECTION_FILES:
    output_name = Path(filename).stem + ".tex"

    converted = convert(
        SECTIONS / filename,
        GENERATED / output_name,
    )

    all_latex.append(converted)


shutil.copy2(
    PAPER / "references.bib",
    ICST / "references.bib",
)

source_figures = ROOT / "results" / "paper" / "figures"

for name in FIGURE_NAMES:
    shutil.copy2(
        source_figures / name,
        FIGURES / name,
    )


combined = "\n".join(all_latex)

if r"\citep{" in combined:
    raise RuntimeError(r"Unconverted \citep found")

if r"\citet{" in combined:
    raise RuntimeError(r"Unconverted \citet found")

if "{[}" in combined:
    raise RuntimeError("Malformed display-math marker found")


longtable_count = combined.count(r"\begin{longtable}")

print(
    "Generated ICST LaTeX fragments:",
    len(SECTION_FILES) + 1,
)

print(
    "Longtable environments:",
    longtable_count,
)

print("Citation normalization: PASS")

print("Display-math normalization: PASS")
