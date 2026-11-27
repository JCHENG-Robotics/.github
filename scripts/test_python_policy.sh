#!/usr/bin/env bash
# Tests the M1 Python allowlist: allowed files pass, everything else fails,
# and path/symlink bypasses are rejected.

set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
policy="$here/check_python_policy.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

pass=0
fail=0

run_case() {
  local name="$1" expected="$2" dir="$3"
  set +e
  bash "$policy" "$dir" >/tmp/python_policy.out 2>&1
  local code=$?
  set -e
  if [[ "$code" -eq "$expected" ]]; then
    echo "PASS: $name (exit $code)"
    pass=$((pass + 1))
  else
    echo "FAIL: $name (exit $code, expected $expected)"
    sed 's/^/  /' /tmp/python_policy.out
    fail=$((fail + 1))
  fi
}

new_case() {
  local name="$1"
  local dir="$tmp/$name"
  mkdir -p "$dir/scripts"
  printf '%s' "$dir"
}

# 1. Both allowed files pass.
d="$(new_case allowed)"
: >"$d/scripts/check_boundaries.py"
: >"$d/scripts/test_check_boundaries.py"
run_case "allowed files" 0 "$d"

# 2. A different Python file fails.
d="$(new_case other)"
: >"$d/scripts/check_boundaries.py"
: >"$d/scripts/other.py"
run_case "unlisted file" 1 "$d"

# 3. A near-miss suffix fails.
d="$(new_case suffix)"
: >"$d/scripts/check_boundaries.py"
: >"$d/scripts/check_boundaries.py.bak"
run_case "unlisted .py.bak" 1 "$d"

# 4. A nested copy at the same basename fails.
d="$(new_case nested)"
mkdir -p "$d/scripts/sub"
: >"$d/scripts/sub/check_boundaries.py"
run_case "nested copy" 1 "$d"

# 5. A hidden Python file fails.
d="$(new_case hidden)"
: >"$d/scripts/.hidden.py"
run_case "hidden file" 1 "$d"

# 6. A symlink to an allowed file under another name fails.
d="$(new_case symlink)"
: >"$d/scripts/check_boundaries.py"
ln -s "$d/scripts/check_boundaries.py" "$d/scripts/evil.py"
run_case "symlink under another name" 1 "$d"

# 7. A symlink at the allowed path fails (no symlink substitution).
d="$(new_case symlink_allowed)"
ln -s /dev/null "$d/scripts/check_boundaries.py"
run_case "symlink at allowed path" 1 "$d"

# 8. A clean governance tree with no Python passes.
d="$(new_case empty)"
run_case "no python" 0 "$d"

echo "allowlist tests: $pass passed, $fail failed"
[[ "$fail" -eq 0 ]]
