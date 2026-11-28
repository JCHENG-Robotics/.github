#!/usr/bin/env bash
# M1 Python policy: .github is a governance repository. Only the two
# report-only boundary-checker files may be Python; every other .py file is
# product code and is rejected.

set -euo pipefail

root="${1:-.}"
root="$(cd "$root" && pwd)"

ALLOW=(
  "scripts/check_boundaries.py"
  "scripts/test_check_boundaries.py"
)

fail=0
while IFS= read -r -d '' path; do
  rel="${path#"$root"/}"
  case "$rel" in
    ./*) rel="${rel#./}" ;;
  esac

  if [[ -L "$path" ]]; then
    echo "ERROR: Python symlink is not allowed in .github: $rel" >&2
    fail=1
    continue
  fi

  allowed=0
  for candidate in "${ALLOW[@]}"; do
    if [[ "$rel" == "$candidate" ]]; then
      allowed=1
      break
    fi
  done

  if [[ "$allowed" -eq 0 ]]; then
    echo "ERROR: Python source outside the governance allowlist: $rel" >&2
    fail=1
  fi
done < <(find "$root" -path "$root/.git" -prune -o \( -type f -o -type l \) \( -name '*.py' -o -name '*.py.*' \) ! -name '*.pyc' -print0)

exit "$fail"
