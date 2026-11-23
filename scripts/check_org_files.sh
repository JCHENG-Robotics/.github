#!/usr/bin/env bash
# M1 gate for the .github repository: structure, no product code, no license,
# no obvious secrets.

set -euo pipefail

fail=0
require_file() {
  if [[ ! -f "$1" ]]; then
    echo "MISSING: $1" >&2
    fail=1
  fi
}

for f in \
  README.md \
  CONTRIBUTING.md \
  CODE_OF_CONDUCT.md \
  SECURITY.md \
  SUPPORT.md \
  GOVERNANCE.md \
  CODEOWNERS.template \
  PULL_REQUEST_TEMPLATE.md \
  LICENSE-REVIEW.md \
  profile/README.md \
  profile/README.zh-CN.md \
  docs/repo-taxonomy.md \
  docs/branch-protection.md \
  docs/release-train.md \
  docs/security-baseline.md \
  docs/hardware-workflow.md \
  docs/license-review.md \
  .github/workflows/reusable-python.yml \
  .github/workflows/reusable-ros-build.yml \
  .github/workflows/reusable-contract-check.yml \
  .github/workflows/reusable-integration-mock.yml \
  .github/workflows/reusable-security.yml \
  .github/workflows/reusable-release.yml \
  .github/workflows/org-health.yml \
  .github/workflows/ci.yml \
  actions/setup-colcon/action.yml \
  actions/contract-manifest/action.yml \
  actions/evidence-check/action.yml \
  ISSUE_TEMPLATE/bug.yml \
  ISSUE_TEMPLATE/feature.yml \
  ISSUE_TEMPLATE/design.yml \
  ISSUE_TEMPLATE/config.yml
do
  require_file "$f"
done

if [[ -e LICENSE ]]; then
  echo "ERROR: LICENSE must not exist before the license review is approved." >&2
  fail=1
fi

if find . -path ./.git -prune -o -name 'package.xml' -print -quit | grep -q .; then
  echo "ERROR: package.xml found; .github must not contain ROS packages." >&2
  fail=1
fi

if find . -path ./.git -prune -o -type f -name '*.py' -print -quit | grep -q .; then
  echo "ERROR: Python source found; M1 .github must not contain product code." >&2
  fail=1
fi

# Obvious secret patterns; skip this script to avoid matching its own regex.
if grep -RIlE \
  --exclude-dir=.git \
  --exclude='check_org_files.sh' \
  'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----' \
  . >/dev/null 2>&1; then
  echo "ERROR: possible secret material found." >&2
  grep -RIlE \
    --exclude-dir=.git \
    --exclude='check_org_files.sh' \
    'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----' \
    . >&2 || true
  fail=1
fi

if [[ "$fail" -ne 0 ]]; then
  echo "M1 .github gate FAILED" >&2
  exit 1
fi
echo "M1 .github gate OK"
