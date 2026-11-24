# Documentation standard

> Applies to every repository in `JCHENG-Robotics`.
> Status: **v1.0 (2026-11-24)**. English is the canonical language of this
> document. Template skeletons live in [`templates/`](templates/).

## 1. Purpose

The ecosystem is split across repositories that are released independently.
A reader must be able to answer four questions without opening the code:

1. **What is this repository, and what is it not?** → `README.md`
2. **Where is it going, and what is next?** → `ROADMAP.md`
3. **What changed, and when?** → `CHANGELOG.md`
4. **What is actually verified, and what is not?** → `ACCEPTANCE.md`

The same four documents, in the same order, with the same status vocabulary,
exist in every product repository. The organization profile
(`.github/profile/README.md`) and the ecosystem-level `ROADMAP.md`,
`CHANGELOG.md` and `ACCEPTANCE.md` in `.github` aggregate the repository-level
documents; they never replace them.

## 2. Required document set

| File | Required in | Notes |
|---|---|---|
| `README.md` | Every repository | English, canonical |
| `README.zh-CN.md` | Every product repository | Chinese translation of `README.md`; English prevails |
| `ROADMAP.md` | Every product repository | Milestones, evidence, next steps |
| `CHANGELOG.md` | Every product repository | Keep a Changelog format |
| `ACCEPTANCE.md` | Every product repository | Root level; `docs/ACCEPTANCE.md` may only be a pointer |

Definitions:

- **Product repository**: a repository with runtime, contract or operations
  content that is versioned and accepted independently: `jcheng-interfaces`,
  `jcheng-system`, `jcheng-manipulation`, `jcheng-mobile`,
  `jcheng-perception`, `jcheng-ops`. New capability repositories join this set
  when they are admitted.
- **Governance repository**: `.github`. It carries the bilingual organization
  profile plus ecosystem-level `ROADMAP.md`, `CHANGELOG.md`, `ACCEPTANCE.md`
  and this standard. It has no `VERSION` and no product acceptance.
- **Bench / staging repository**: an explicitly labelled sandbox such as
  `jcheng-mobile-bench`. It needs a `README.md` that states its status and
  what it is not; the other three documents are not required because nothing
  in it is released or accepted.

Every required document starts with a short status block; `CHANGELOG.md` starts
with the format note instead (see §8):

```markdown
> Status: **<state>** as of <YYYY-MM-DD>. <one sentence of scope>.
> English canonical; see README.zh-CN.md for the Chinese translation.
```

## 3. Language policy

- `README.md` is written in English and is canonical. `README.zh-CN.md` is a
  full translation and opens with a pointer: “本文为英文主文档的中文对照；如有
  歧义，以英文版为准。”
- `ROADMAP.md`, `CHANGELOG.md` and `ACCEPTANCE.md` are English-only. This keeps
  status and acceptance claims in one language, so they cannot drift apart.
- Code comments, commit messages, log excerpts and command output stay in
  their original language. Do not translate quoted evidence.
- Chinese-only source material that predates this standard may remain under
  `docs/` as reference; the root documents above are still required.

## 4. Status vocabulary

Use only these terms. Do not invent synonyms.

| Dimension | Values | Meaning |
|---|---|---|
| Delivery | `Complete`, `In progress`, `Planned`, `Not started` | Milestone state |
| Verification | `Verified`, `Partially verified`, `Unverified`, `Inconclusive` | Claim state |
| Evidence class | `L0`–`L5` | See §7 |
| Repository state | `Experimental`, `Deployed`, `Frozen`, `Archived` | Release posture |

Rules:

- A capability with only synthetic or mock evidence is **not** `Verified`.
  Write `Partially verified (synthetic)` or `Unverified`.
- `Verified` requires a linked evidence path and the date it was produced.
- “Not hardware-validated” is stated explicitly, not implied.
- Dates are ISO 8601 (`2026-11-24`).

## 5. README.md

Required sections, in this order. Sections that do not apply are still listed
with `Not applicable` so the structure stays comparable.

1. **Title and one-paragraph purpose.**
2. **Status block** — state, date, version, and the single most important
   limitation.
3. **Scope and boundary** — a table of inputs, outputs, owned devices and
   forbidden actions. State `hardware_access` from `capability.yaml`.
4. **Repository layout** — a short tree; no more than two levels deep.
5. **Requirements** — OS, ROS distribution, runtime dependencies, hardware.
6. **Quick start** — build, run and test commands that work without hardware.
7. **Validation status** — verified / partially verified / unverified, each
   with a pointer to `ACCEPTANCE.md`.
8. **Related repositories** — layer, upstream contracts and consumers.
9. **License** — current status (`pending` until the review closes).

Do not put a full changelog or a full milestone history in the README. Link
to `CHANGELOG.md` and `ROADMAP.md` instead.

## 6. ROADMAP.md

Required sections:

1. **Status block** — current version, last updated date.
2. **Current state** — one table of what is delivered and what is still open.
3. **Milestones** — `M0`…`Mn` with scope, state, evidence link and exit
   criterion. Completed milestones keep their evidence link.
4. **Next** — the next one or two milestones only, with prerequisites.
5. **Out of scope** — what this repository will not do, including forbidden
   cross-layer responsibilities.
6. **Dependencies** — contract versions, system API range, operator
   authorization requirements.

Milestone numbering is repository-local. Ecosystem milestones are tracked in
`.github/ROADMAP.md`; repository documents reference them but do not redefine
them.

## 7. ACCEPTANCE.md

Acceptance is layered. Every result carries a level:

| Level | Name | Environment | Hardware |
|---|---|---|---|
| L0 | Contract / static | CI runner | No |
| L1 | Unit | CI runner | No |
| L2 | Mock integration | In-process / mock bus | No |
| L3 | Mock end-to-end | Mock gateway / topics | No |
| L4 | Replay | Recorded data | No |
| L5 | Hardware | Robot | Yes |

Required sections:

1. **Status block** — version, date, operator, reviewer, result
   (`pass` / `fail` / `inconclusive`).
2. **Scope** — which claims this report covers.
3. **Gate results** — table: gate, command, level, result, evidence.
4. **Verified claims** — each with level and evidence path.
5. **Not verified** — explicit list with the reason and the risk.
6. **Limitations** — safety and validity limits that remain true.
7. **Sign-off** — operator and reviewer, or `pending`.
8. **Machine-readable report** — if a JSON report is produced, it must validate
   against
   [`acceptance-report.v1.schema.json`](https://github.com/JCHENG-Robotics/jcheng-interfaces/blob/main/schemas/acceptance-report.v1.schema.json).

Hard rules:

- Synthetic, mock and replay results are never reported as hardware
  validation.
- A failed bound stays failed. Do not replace it with a more favourable
  statistic.
- `pass` requires every required gate at its declared level to pass. A skipped
  optional gate is listed, not hidden.
- Hardware acceptance requires the operator's explicit authorization and is
  recorded per session.
- Repositories that do not command motion say so in the status block.

## 8. CHANGELOG.md

Format: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) with
[Semantic Versioning](https://semver.org/).

- One `## [Unreleased]` section at the top, then released versions newest
  first: `## [0.1.0] — 2026-11-23`.
- Groups in this order: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`,
  `Security`.
- Every entry states the observable change, not the implementation diary.
  Link evidence or the PR when it helps.
- Do not put acceptance status, limitations or “not verified” notes in the
  changelog. Those belong in `ACCEPTANCE.md`.
- A release entry names the tag and the contract version it pins.

## 9. Links and cross-references

- Relative links inside a repository.
- Absolute links to `https://github.com/JCHENG-Robotics/<repo>/blob/main/...`
  across repositories. Do not link to feature branches from released
  documents.
- Every document ends with a `Related` list: contract repository, system
  repository, operations repository, and the ecosystem documents in
  `.github`.
- Links must resolve. The repository gate checks relative links; reviewers
  check cross-repository links.

## 10. Change process

- Documentation changes follow `CONTRIBUTING.md`: PR, one reviewer, no direct
  push to `main`.
- A change to scope, safety semantics or acceptance status updates
  `README.md`, `ROADMAP.md` and `ACCEPTANCE.md` in the same PR.
- A version release updates `VERSION`, `CHANGELOG.md` and the tag together.
- The standard itself is versioned in this file; changes are recorded in
  `.github/CHANGELOG.md`.
