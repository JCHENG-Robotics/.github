# Final Regression Report — Fixed Main

> Date: 2026-11-28. Clean worktrees were created from each repository's
> `origin/main` at the SHAs in 42. Counts below are from those main trees; the
> candidate PR counts are shown separately. Historical branch counts are not
> added together.

## 1. Results

| Repository | Command | Result | Gate |
|---|---|---|---|
| interfaces | `pytest -q` | **16 passed** | gate OK; 25 IDL files |
| devices | `pytest -q` | **120 passed** (candidate #7: 122) | gate OK |
| scenarios | `pytest -q` | **116 passed** | gate OK |
| applications | `pytest -q` | **211 passed, 5 skipped** (candidate #20: 218 + 5) | gate OK |
| system | `pytest -q` | **191 passed** | gate OK |
| mobile | `pytest -q` | **50 passed** | no gate script |
| studio | `pytest -q tests`; backend venv | **13 + 222 passed** | gate OK |
| perception | `pytest -q` | **107 passed** | no gate script |
| learning | `uv sync --frozen --extra test`; pytest | **68 passed** | gate OK |
| teleop | `pytest -q` | **218 passed** | gate OK |
| simulation | `pytest -q` | **86 passed, 2 skipped** | gate OK |
| benchmark | `pytest -q` | **61 passed** | gate OK |
| ops | `pytest -q` | **9 passed** | gate OK |
| research | pytest (none) | no tests | gate OK |
| `.github` | `pytest -q` | **20 passed** | Python policy OK |
| frozen baseline | tag `v1.0.0` | `b3411e4…`, exact tag | integrity present |

Environment: Ubuntu 24.04.5, Python 3.12.3, ROS 2 Jazzy (not required by most
tests), offline. Commands and logs are reproducible from `dev/test.sh` and the
repository gates; learning uses its frozen `uv` environment.

## 2. Governance

`check_boundaries.py --mode report --root /tmp/b1-reg`:

- **25 open**, **1 waived** (studio B4, waiver `W-2026-11-27-01`).
- 0 open findings introduced by the Baseline 1 candidate changes.
- The findings are known debt (schema ownership, device-fact copies in
  learning/teleop/simulation/studio, capability manifest shape, deployed
  contract skew). They are recorded, not hidden.

The boundary run is report-only: findings do not fail the command, and
`check_python_policy.sh` passes.

## 3. Artifact integration

The real CLI chain on pristine main passed (44). The candidate mock task passed
all eight cases (45). The negative tests (stale hash, wrong unit, missing role,
threshold mismatch, unauthorized run) fail closed as required.

## 4. Frozen baseline

`jcheng-manipulation` tag `v1.0.0` resolves to
`b3411e43ad31c09f396cdd2db0fdfda8f09853dd` and is an exact tag. The repository's
`origin/main` is a different commit (`d63f6d1`) from the design line; the frozen
tag is the Baseline 1 reference and was not modified.

## 5. Interpretation

All test suites pass on the fixed main baseline and on the candidate branches.
The remaining gates are human review/approval, not test failures. Deployment
evidence is out of scope and unchanged.
