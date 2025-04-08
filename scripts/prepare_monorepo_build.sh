#!/bin/sh
# This script change all pyproject.toml to pin the local dependencies
set -x
set -u
set -e
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "${DIR}/.." || exit

poetry version
VERSION=$(poetry version | awk '{print $2}')

if [ "$(uname)" = "Darwin" ]; then export SEP=" "; else SEP=""; fi

# all python packages, in topological order
. ${DIR}/projects.sh
_projects=$PROJECTS
echo "Running on following projects: ${_projects}"
for p in $_projects
do
  cd "${DIR}/../${p}" || exit
  # change path deps in project def
  sed -i$SEP'' "s|{.*path.*|\"^$VERSION\"|" pyproject.toml
done
