#!/bin/sh
# runs the passed command in each poetry project folder
# set -x
set -u
set -e
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "${DIR}/.." || exit

# all python packages, in topological order
. "${DIR}/projects.sh"
_projects="${PROJECTS}"
echo "Running on following projects: ${_projects}"
for p in $_projects
do
  cd "${DIR}/../${p}" || (echo "ERROR!!! Project ${p} doesn't exist" && exit 2)
  echo "=== running in ${p} $> poetry $@ ==="
  poetry $@
done
