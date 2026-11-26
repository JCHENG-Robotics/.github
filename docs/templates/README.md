# <Repository name>

**English** | [简体中文](README.zh-CN.md)

<One paragraph: what this repository is, in one sentence of scope and one sentence of boundary.>

> Status: **<Experimental | Deployed | Frozen>** as of <YYYY-MM-DD>.
> Version <x.y.z>. <The single most important limitation.>
> English canonical; the Chinese README is a translation.

## Scope and boundary

| Item | This repository |
|---|---|
| Layer | L<0–4> |
| Inputs | <topics / APIs / files> |
| Outputs | <topics / APIs / files> |
| Hardware access | `<none | camera_readonly | ...>` (`capability.yaml`) |
| Owned devices | <none, or the exact device> |
| Forbidden | <device access, motion topics, vendor code> |

## Repository layout

```text
<repo>/
├── capability.yaml
├── VERSION
├── README.md
├── README.zh-CN.md
├── ROADMAP.md
├── CHANGELOG.md
├── ACCEPTANCE.md
└── <source tree>
```

## Requirements

- <OS / ROS distribution>
- <runtime dependencies>
- <hardware, if any>

## Quick start

```bash
<build>
<test>
<run without hardware>
```

## Validation status

| Claim | Status | Evidence |
|---|---|---|
| <claim> | <Verified | Partially verified | Unverified> | <path> |

Full report: [ACCEPTANCE.md](ACCEPTANCE.md).

## Related repositories

- [`jcheng-interfaces`](https://github.com/JCHENG-Robotics/jcheng-interfaces) — contract source.
- [`jcheng-system`](https://github.com/JCHENG-Robotics/jcheng-system) — privileged runtime.
- [`jcheng-ops`](https://github.com/JCHENG-Robotics/jcheng-ops) — operations.
- [`.github`](https://github.com/JCHENG-Robotics/.github) — ecosystem roadmap, changelog and acceptance.

## License

Pending third-party and copyright review; no `LICENSE` file has been added.
See [LICENSE-REVIEW.md](LICENSE-REVIEW.md).
