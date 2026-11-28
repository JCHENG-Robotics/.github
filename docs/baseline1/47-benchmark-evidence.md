# Benchmark Evidence Report

> Offline synthetic evidence. The observed suite is INCONCLUSIVE by design; the
> PASS/FAIL suites use test-only thresholds.

## 1. Traceability fields

The benchmark CLI report itself carries the suite/dataset hashes and its own
timestamp. The surrounding evidence package adds:

| Field | Where |
|---|---|
| scenario_id / scenario_version | every sample in `samples.jsonl`; task summary |
| evaluation_id | every sample; task summary |
| cell composition | task summary and reference report |
| device source hashes | reference report / task summary artifacts |
| artifact hashes | reference report / task summary artifacts |
| task status / failure reason | 8-case task summary |
| data source | `synthetic` in suite, samples and task summary |
| run environment | offline loopback mock, `evidence_class: L2` |
| experiment time | benchmark report timestamp |
| repository SHAs | `task_summary.repository_shas` (devices, scenarios, applications, benchmark) |
| evaluation threshold source | observed: none; test-pass/fail: explicitly test-only |

The benchmark report does **not** embed scenario/evaluation IDs itself; the
dataset it hashes does, so the link is traceable through the verified dataset
hash. This is stated explicitly rather than overclaimed.

## 2. Observed suite

`benchmark-observed`: no thresholds, 8 synthetic samples, success rate 0.125
(1/8). Result **inconclusive**. This is a valid result; it is not a failure and
not a pass.

## 3. Discrimination suites

| Suite | Threshold | Result | Report |
|---|---|---|---|
| `ore-sorting-mock-test-pass` | success_rate ≥ 0.10 | pass | `benchmark-test-pass/benchmark_report.json` |
| `ore-sorting-mock-test-fail` | success_rate ≥ 0.99 | fail | `benchmark-test-fail/benchmark_report.json` |

The benchmark CLI exit codes were 0/1/2 respectively and each report hashed the
exact suite and dataset it was given (`run_benchmark` verifies both hashes).

## 4. Interpretation

The harness can distinguish PASS, FAIL and INCONCLUSIVE, and the observed data
is honestly inconclusive. The test thresholds are not ore-sorting business
acceptance criteria and must not be quoted as such.

Evidence: `~/jcheng/phase2/baseline1-acceptance-20261128/mock-task/benchmark-*`
and `.../reference/benchmark_report.json`.
