# Final Main Regression Report

> Fixed `origin/main` after the four Baseline 1 merges. Clean detached
> worktrees were used; historical branch counts are not added to this result.

## 1. Fixed main SHAs

| Repository | main SHA |
|---|---|
| `.github` | `f9e77eb8b309ab705c20f08a34bb28be68ff8ce7` |
| interfaces | `426f3713e8f3bfbc024982a2f1372c555a82fa92` |
| devices | `c4be89747794fa6aca1a5fd101a999d7e75be14b` |
| scenarios | `1c218858fd4e90792cd9de9b5a45af25c8faa4f9` |
| applications | `0be306e7d7ebf7b8a7e6b47aa5fb0c518358d90c` |
| system | `72b2ce25266d3463d4590e871f6a2905fd938704` |
| mobile | `f96cfee2a3330d6a830f9807f92dc0539ee5d7be` |
| studio | `40c002b02131e56b1a4923c8a5f75a2beb26909c` |
| perception | `343e621298518f8dbc7c02873f11885bb9de2fa4` |
| learning | `69978259f8d6bbfa21f472a4d139bd6798a6f10b` |
| teleop | `984b12f5c96d39462b6f6ecf33d4c914bdd75684` |
| simulation | `40c250d93fdb72a5088e2c71f3dcb263c791eb0c` |
| benchmark | `bfaeac9ee4cb9f5cd5b555b21ec08e1e8d9645e7` |
| ops | `4d365f6bd354a1a6cefc676da92d648d73c973c3` |
| research | `58858ecea618fb0dd12bda84d39db49bf0ded2b6` |
| manipulation | tag `v1.0.0` = `b3411e43ad31c09f396cdd2db0fdfda8f09853dd` |

## 2. Tests and gates

| Repository | Result | Gate |
|---|---|---|
| interfaces | 22 passed | OK |
| devices | 123 passed | OK |
| scenarios | 116 passed | OK |
| applications | 218 passed, 5 skipped | OK |
| system | 191 passed | OK |
| mobile | 50 passed | no gate script |
| studio | 13 + 222 passed | OK |
| perception | 107 passed | no gate script |
| learning | 68 passed (frozen uv env) | OK |
| teleop | 218 passed | OK |
| simulation | 86 passed, 2 skipped | OK |
| benchmark | 61 passed | OK |
| ops | 9 passed | OK |
| research | no tests | OK |
| `.github` | 20 passed | Python policy OK |

Environment prerequisites: learning needs `UV_PROJECT_ENVIRONMENT` outside the
repo (an in-tree `.venv` fails the gate's large-file/broken-link check);
studio's 222 backend tests need the out-of-tree main venv. `dev/test.sh studio`
silently skips the backend tests in a clean worktree, so the 13+222 count
assumes that venv. Neither is a code failure.

## 3. Acceptance entry

```bash
DEVICES_ROOT=... SCENARIOS_ROOT=... APPLICATIONS_ROOT=... \
BENCHMARK_ROOT=... SIMULATION_ROOT=... OUT=... \
.github/dev/baseline1-acceptance.sh
```

Result on fixed main (`/tmp/b1-evidence/final-main-f9e77eb`):

- reference `matched_with_unverified`, 2 steps, mock SUCCEEDED,
  benchmark inconclusive, simulation not_checked;
- 8/8 mock cases expected; benchmark observed/test-pass/test-fail =
  inconclusive/pass/fail;
- gates `offline_execution_allowed: true`, `deployment_ready: false`,
  `motion_authorized: false`.

## 4. Negative tests

`STALE_DEVICE_HASH`, `INCOMPATIBLE_UNIT`, `INCOMPATIBLE_PARAMETER`, and an
unauthorized mock run (`ABORTED`, zero execute) fail closed. `NO_DEVICE_FOR_ROLE`
was verified by a manual CLI run; it is not yet an automated pytest (P3).

## 5. Governance

`check_boundaries.py --mode report` on the 16-repository main workspace:
**25 open + 1 waived** (studio B4 waiver until 2026-12-31). No new Baseline 1
finding was introduced. Report-only; findings do not fail the command.

## 6. Not in this main run

The AR5L/AR5R registration (#8), vocabulary (#5) and contract ratification (#21)
are merged into the fixed main above. The nine-device registry and the
`contracted` requirements are part of this evidence; only the freeze record PR
remains unmerged.
