from pathlib import Path

PAPER = Path("paper")
SECTIONS = PAPER / "sections"

TITLE = (
    "Residual-Risk-Guided Discovery of Stochastic Mixed-Order Capability Interactions"
)

ORDER = (
    "08_abstract.md",
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


FIGURES = {
    "## RQ1 — Holdout Discovery Accuracy": """
![SCIF V4 exact recovery on the 1,000-seed unseen holdout.](../results/paper/figures/figure_5_holdout_recovery.png)

*Figure 1. SCIF v0.0.4 exact recovery across the seven 1,000-seed unseen holdout scenarios.*
""",
    "## RQ2 — Comparison with Discovery Baselines": """
![Exact interaction recovery by discovery method.](../results/paper/figures/figure_1_recovery_comparison.png)

*Figure 2. Exact recovery of SCIF V3, deletion localization, exhaustive discovery, and SCIF V4.*

![Simulator execution cost by discovery method.](../results/paper/figures/figure_2_execution_comparison.png)

*Figure 3. Mean simulator executions required by each discovery method.*
""",
    "## RQ5 — Scaling Behavior": """
![SCIF V4 execution scaling compared with exhaustive order-three search.](../results/paper/figures/figure_3_scaling.png)

*Figure 4. Simulator execution scaling from 8 to 20 capabilities.*

![Execution reduction relative to exhaustive discovery.](../results/paper/figures/figure_4_scaling_reduction.png)

*Figure 5. Relative execution reduction of SCIF V4 compared with exhaustive order-three discovery.*
""",
}


TABLE_CAPTIONS = {
    "| Scenario | Exact Recovery | False-Positive Runs | Mean Executions |": (
        "**Table 1. Holdout exact recovery and execution cost.**\n\n"
    ),
    "| Scenario | Method | Recovery | Mean Executions |": (
        "**Table 2. Method comparison over 100 seeds per scenario.**\n\n"
    ),
    "| Scenario | V3 Pairwise Only | V3 + Residual | Full V4 |": (
        "**Table 3. Ablation of residual-risk detection and localization.**\n\n"
    ),
    "| Capabilities | Exact Recovery | Mean SCIF V4 Executions | Exhaustive Executions | Reduction |": (
        "**Table 4. Scaling of recovery and simulator execution cost.**\n\n"
    ),
}


def inject_figures(
    text: str,
) -> str:
    for heading, figure in FIGURES.items():
        marker = f"{heading}\n"

        if marker not in text:
            raise RuntimeError(f"Figure insertion heading not found: {heading}")

        text = text.replace(
            marker,
            marker + figure + "\n",
            1,
        )

    return text


def inject_table_captions(
    text: str,
) -> str:
    for header, caption in TABLE_CAPTIONS.items():
        if header not in text:
            raise RuntimeError(f"Table header not found: {header}")

        text = text.replace(
            header,
            caption + header,
            1,
        )

    return text


parts = [
    f"# {TITLE}",
    "",
    "**Berliant Research Prototype — SCIF v0.0.4**",
    "",
    "---",
    "",
]

for index, filename in enumerate(ORDER):
    path = SECTIONS / filename

    if not path.exists():
        raise FileNotFoundError(path)

    content = path.read_text(encoding="utf-8")

    if filename == "04_results.md":
        content = inject_figures(content)

        content = inject_table_captions(content)

    parts.append(content.rstrip())

    if index < len(ORDER) - 1:
        parts.extend(
            (
                "",
                "---",
                "",
            )
        )


output = PAPER / "manuscript.md"

output.write_text(
    "\n".join(parts) + "\n",
    encoding="utf-8",
)

print(
    "Built:",
    output,
)

print(
    "Words:",
    len(output.read_text(encoding="utf-8").split()),
)
