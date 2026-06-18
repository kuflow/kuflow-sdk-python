#!/usr/bin/env sh
#
# Pre-flight check for the Python interpreter AutoRest will use to build the
# @autorest/python generator venv.
#
# AutoRest creates that venv with `--copies` (NOT symlinks). A copied venv only
# works if the interpreter is "normally" linked: it must have `ensurepip` and a
# libpython that the copied binary can still find. python-build-standalone
# builds (mise/uv) embed a `$ORIGIN/../lib/libpython*.so` NEEDED entry, so their
# copied venvs fail with "error while loading shared libraries" (exit 127).
#
# This check reproduces what AutoRest does and fails LOUDLY (and early) with a
# clear message instead of letting AutoRest die on an unreadable stack trace.

set -e

PY="${AUTOREST_PYTHON_EXE:-/usr/bin/python3}"

fail() {
  echo ""                                                                          1>&2
  echo "################################################################################" 1>&2
  echo "##  AUTOREST PYTHON CHECK FAILED"                                          1>&2
  echo "################################################################################" 1>&2
  echo ""                                                                          1>&2
  echo "  AutoRest needs a Python able to create a working venv with --copies"     1>&2
  echo "  (it needs 'ensurepip' AND a normally-linked libpython)."                 1>&2
  echo ""                                                                          1>&2
  echo "  Interpreter tried : $PY"                                                 1>&2
  echo "  Reason            : $1"                                                   1>&2
  echo ""                                                                          1>&2
  echo "  How to fix:"                                                             1>&2
  echo "    * Install the venv module on the system Python:"                       1>&2
  echo "        sudo apt install python3-venv      # or python3.12-venv"           1>&2
  echo ""                                                                          1>&2
  echo "    * OR point AUTOREST_PYTHON_EXE to a normally-linked Python >= 3.8"     1>&2
  echo "      that has ensurepip. Do NOT use a python-build-standalone build"      1>&2
  echo "      (mise / uv): its copied venvs cannot find libpython (exit 127)."     1>&2
  echo ""                                                                          1>&2
  echo "################################################################################" 1>&2
  echo ""                                                                          1>&2
  exit 1
}

# 1. Interpreter exists and is runnable.
[ -x "$PY" ] || command -v "$PY" >/dev/null 2>&1 || fail "interpreter not found or not executable"

# 2. Reproduce exactly what AutoRest does: a --copies venv that can run pip.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

"$PY" -m venv --copies "$TMP/venv" >/dev/null 2>&1 \
  || fail "could not create a '--copies' venv (is 'ensurepip' / python3-venv installed?)"

"$TMP/venv/bin/python" -m pip --version >/dev/null 2>&1 \
  || fail "the copied venv's python cannot run pip (libpython not found? python-build-standalone build?)"

echo "✓ AutoRest python check passed: $PY"
