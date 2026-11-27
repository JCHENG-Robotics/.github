# Learning Regression Report — isolated environment

> Status: **pass (L1 offline only)**. Full detail lives in the Learning
> repository; this is the ecosystem-level record.

| Item | Value |
|---|---|
| Repository | `jcheng-learning` |
| Branch / PR | `feat/regression-20261127` / [#5](https://github.com/JCHENG-Robotics/jcheng-learning/pull/5) |
| Environment | Python 3.12.3, venv at `/tmp/jcheng-learning-venv` (outside repo) |
| Sync | `uv sync --frozen --extra test --python 3.12` |
| Test | `uv run --frozen --extra test --python 3.12 python -m pytest tests -q` |
| Lock | `uv.lock` sha256 `a866bfd1…` (unchanged) |
| pyarrow | 24.0.0 |
| Result | **68 passed**; repository gate OK |
| Report | `jcheng-learning/docs/REGRESSION-20261127.md` |
| CI | `learning-gate` success on the PR head |

Root cause: the host interpreter lacked the project dependencies; `pyarrow` is
a required dependency. A second pitfall was `uv run pytest` resolving the system
`pytest`; the gate correctly uses `uv run --frozen --extra test python -m pytest`.

No `pyproject.toml`/`uv.lock` change, no system-Python install, no sudo, no
dependency upgrade. The venv and caches are outside the repository and are not
committed. This is not a ROS, Gazebo or hardware validation.

## Related

- [Contract & regression report](11-contract-regression-report.md)
- [Independent QA](18-independent-qa-report.md)
