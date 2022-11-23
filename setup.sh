#!/bin/zsh

# Check if this is sourced
(
 [[ -n $ZSH_EVAL_CONTEXT && $ZSH_EVAL_CONTEXT =~ :file$ ]] ||
 [[ -n $BASH_VERSION ]] && (return 0 2>/dev/null)
) && SOURCED=1 || SOURCED=0
if [[ $SOURCED == 0 ]]; then
    msg="This script is not sourced. to use it run : source $0"
    echo -e "\033[1;31m${msg}\033[0m"
	  exit 1
fi

SCRIPT_PATH="$( cd "$(dirname ${BASH_SOURCE[0]} 2> /dev/null || dirname ${(%):-%N})" && pwd -P )"

cd "${SCRIPT_PATH}" || return 1

PYTHON_BIN="$(which python >/dev/null && echo "python" || echo "python3")"
${PYTHON_BIN} -m venv venv || return 1

source venv/bin/activate

pip install .
