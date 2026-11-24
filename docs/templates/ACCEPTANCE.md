# Acceptance report

> Status: **<pass | fail | inconclusive>** as of <YYYY-MM-DD> for v<x.y.z>.
> Operator: <name>. Reviewer: <name | pending>.
> Scope: <which claims this report covers>.
> <State "no motion commands were sent" when true.>

## 1. Gates

| Gate | Command | Level | Result | Evidence |
|---|---|---|---|---|
| Contract / static | `<command>` | L0 | <pass | fail | inconclusive> | <path> |
| Unit | `<command>` | L1 | <result> | <path> |
| Mock integration | `<command>` | L2 | <result> | <path> |
| Mock end-to-end | `<command>` | L3 | <result> | <path> |
| Replay | `<command>` | L4 | <result> | <path> |
| Hardware | `<command>` | L5 | <result> | <path> |

## 2. Verified claims

| Claim | Level | Evidence |
|---|---|---|
| <claim> | L<0–5> | <path> |

## 3. Not verified

| Item | Reason | Risk |
|---|---|---|
| <item> | <why> | <consequence> |

## 4. Limitations

- <Safety or validity limit that remains true.>

## 5. Sign-off

| Role | Name | Date |
|---|---|---|
| Operator | <name> | <YYYY-MM-DD> |
| Reviewer | <name | pending> | <YYYY-MM-DD> |

## 6. Machine-readable report

<Path to the JSON report, or “none”. It must validate against
`acceptance-report.v1.schema.json` in `jcheng-interfaces`.>
