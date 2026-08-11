import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICST = ROOT / "paper" / "icst"
GENERATED = ICST / "generated"

SOURCE_BUILDER = ROOT / "experiments" / "build_icst_sources.py"


TABLES = (
    r"""
\begin{table*}[t]
\caption{Holdout exact recovery and execution cost.}
\label{tab:holdout}
\centering
\footnotesize
\setlength{\tabcolsep}{8pt}
\begin{tabular}{lrrr}
\toprule
Scenario & Exact Recovery & FP Runs & Mean Executions \\
\midrule
NULL     & 1000/1000 (100\%) & 0/1000 & 4,907.6 \\
PAIR-001 & 1000/1000 (100\%) & 0/1000 & 10,800.0 \\
PAIR-002 & 999/1000 (99.9\%)  & 0/1000 & 10,946.2 \\
PAIR-003 & 1000/1000 (100\%) & 0/1000 & 10,846.2 \\
OVERLAP  & 1000/1000 (100\%) & 0/1000 & 13,100.0 \\
TRIPLE   & 1000/1000 (100\%) & 0/1000 & 17,712.3 \\
MIXED    & 1000/1000 (100\%) & 0/1000 & 22,803.2 \\
\bottomrule
\end{tabular}
\end{table*}
""",
    r"""
\begin{table*}[t]
\caption{Method comparison over 100 seeds per scenario.}
\label{tab:comparison}
\centering
\footnotesize
\setlength{\tabcolsep}{9pt}
\begin{tabular}{llrr}
\toprule
Scenario & Method & Recovery & Mean Executions \\
\midrule
PAIR-002 & SCIF V3    & 100\% & 7,900 \\
PAIR-002 & Deletion   & 2\%   & 9,570 \\
PAIR-002 & Exhaustive & 100\% & 37,000 \\
PAIR-002 & SCIF V4    & 100\% & 10,900 \\
\addlinespace
OVERLAP & SCIF V3    & 100\% & 10,100 \\
OVERLAP & Deletion   & 0\%   & 9,000 \\
OVERLAP & Exhaustive & 100\% & 37,000 \\
OVERLAP & SCIF V4    & 100\% & 13,100 \\
\addlinespace
TRIPLE & SCIF V3    & 0\%   & 3,700 \\
TRIPLE & Deletion   & 100\% & 13,000 \\
TRIPLE & Exhaustive & 100\% & 93,000 \\
TRIPLE & SCIF V4    & 100\% & 17,700 \\
\addlinespace
MIXED & SCIF V3    & 0\%   & 7,800 \\
MIXED & Deletion   & 0\%   & 9,000 \\
MIXED & Exhaustive & 100\% & 93,000 \\
MIXED & SCIF V4    & 100\% & 22,800 \\
\bottomrule
\end{tabular}
\end{table*}
""",
    r"""
\begin{table*}[t]
\caption{Ablation of residual-risk detection and localization.}
\label{tab:ablation}
\centering
\footnotesize
\setlength{\tabcolsep}{8pt}
\begin{tabular}{lccc}
\toprule
Scenario & V3 Pairwise Only & V3 + Residual & Full V4 \\
\midrule
NULL     & 100\% & 100\% & 100\% \\
PAIR-002 & 100\% & 100\% & 100\% \\
OVERLAP  & 100\% & 100\% & 100\% \\
TRIPLE   & 0\% & 100\% escalation & 100\% exact \\
MIXED    & 0\% & 100\% escalation & 100\% exact \\
\bottomrule
\end{tabular}
\end{table*}
""",
    r"""
\begin{table*}[t]
\caption{Scaling of recovery and simulator execution cost.}
\label{tab:scaling}
\centering
\footnotesize
\setlength{\tabcolsep}{7pt}
\begin{tabular}{rrrrr}
\toprule
Capabilities &
Exact Recovery &
Mean SCIF V4 &
Exhaustive &
Reduction \\
\midrule
8  & 20/20 (100\%) & 22,800 & 93,000    & 75.48\% \\
12 & 20/20 (100\%) & 31,000 & 299,000   & 89.63\% \\
16 & 20/20 (100\%) & 40,800 & 697,000   & 94.15\% \\
20 & 20/20 (100\%) & 52,200 & 1,351,000 & 96.14\% \\
\bottomrule
\end{tabular}
\end{table*}
""",
)


def build_sources() -> None:
    subprocess.run(
        [
            sys.executable,
            str(SOURCE_BUILDER),
        ],
        cwd=ROOT,
        check=True,
    )


def replace_tables() -> None:
    path = GENERATED / "04_results.tex"

    text = path.read_text(
        encoding="utf-8",
    )

    pattern = re.compile(
        r"\\begin\{longtable\}"
        r".*?"
        r"\\end\{longtable\}",
        re.DOTALL,
    )

    blocks = pattern.findall(text)

    if len(blocks) != 4:
        raise RuntimeError(f"Expected 4 longtables, found {len(blocks)}")

    for block, table in zip(
        blocks,
        TABLES,
        strict=True,
    ):
        text = text.replace(
            block,
            table.strip(),
            1,
        )

    if r"\begin{longtable}" in text:
        raise RuntimeError("Longtable remains after conversion")

    path.write_text(
        text,
        encoding="utf-8",
    )

    print("IEEE table conversion: PASS")


def write_main() -> None:
    main = r"""
\documentclass[conference]{IEEEtran}

\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{cite}
\usepackage[hidelinks]{hyperref}

\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}%
  \setlength{\parskip}{0pt}%
}

\title{
Residual-Risk-Guided Discovery of
Stochastic Mixed-Order Capability Interactions
}

\author{
\IEEEauthorblockN{Anonymous Author(s)}
\IEEEauthorblockA{Anonymous Submission}
}

\begin{document}

\maketitle

\begin{abstract}
\input{generated/08_abstract.tex}
\end{abstract}

\input{generated/00_introduction.tex}

\input{generated/01a_related_work.tex}

\input{generated/01_research_questions.tex}

\input{generated/02_methodology.tex}

\input{generated/03_experimental_setup.tex}

\input{generated/04_results.tex}

\begin{figure}[t]
\centering
\includegraphics[
  width=0.94\columnwidth
]{figures/figure_1_recovery_comparison.pdf}
\caption{
Exact interaction recovery by discovery method.
}
\label{fig:recovery}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[
  width=0.94\columnwidth
]{figures/figure_2_execution_comparison.pdf}
\caption{
Mean simulator executions by discovery method.
}
\label{fig:executions}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[
  width=0.94\columnwidth
]{figures/figure_3_scaling.pdf}
\caption{
Simulator execution scaling from 8 to 20 capabilities.
}
\label{fig:scaling}
\end{figure}

\input{generated/05_discussion.tex}

\input{generated/06_limitations_and_threats.tex}

\input{generated/07_conclusion.tex}

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
""".lstrip()

    path = ICST / "main.tex"

    path.write_text(
        main,
        encoding="utf-8",
    )

    print("ICST main.tex: PASS")


build_sources()
replace_tables()
write_main()

print("ICST paper source build complete.")
