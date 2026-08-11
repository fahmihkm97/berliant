# Environment

Reference development environment:

- Operating system: Ubuntu 22.04 under WSL2
- Python: 3.12
- package and environment manager: uv

The exact dependency graph is recorded in:

    uv.lock

Install the environment with:

    uv sync

Verify the main tools with:

    uv run python --version
    uv run ruff --version
    uv run mypy --version
    uv run pytest --version

All Python project commands should be executed through `uv run`.
