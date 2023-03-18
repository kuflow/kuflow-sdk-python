#!/bin/sh
# This script reflects the latest changes of pyproject.toml
#  into both the poetry.lock file and the virtualenv.
#  by running `poetry update && poetry install --sync`
# It first configures poetry to use the right python for creation of the virtual env

# xtrace: Print each command before it is executed.
set -x

# nounset: if an attempt is made to expand an unset variable, the shell will print an error message and exit with a non-zero status
set -u

# errexit: Exist on error
set -e

command_exists () {
    command -v $1 >/dev/null 2>&1;
}

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "${DIR}/.." || exit

# all python packages, in topological order
. ${DIR}/projects.sh
_projects=". ${PROJECTS}"
echo "Running on following projects: ${_projects}"
for p in $_projects
do
  cd "${DIR}/../${p}" || exit

  # Check if we have pyenv
  if command_exists pyenv; then
    echo "Pyenv detected"
    (pyenv local && poetry env use $(which python)) || poetry env use 3.8
  else
    echo "Using python: $(which python)"
    (poetry env use $(which python)) || poetry env use 3.8
  fi

  poetry update && poetry install --sync
done
