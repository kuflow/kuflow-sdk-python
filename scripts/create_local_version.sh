#!/bin/sh
# To use: Set the appropriate version
# Usefully when building wheels in CI/CD on branches or merge requests,
# without possibly overwriting released versions (of certain tag)
# Used to run in CI/CD, as it will modify both pyproject.toml's and python files (by setting the right string in `__version__=..`)
# Dev version follow the patter: X.X.X.devX

########################################
VERSION=0.8.3
########################################


set -x
set -u
set -e
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "${DIR}/.." || exit


# all python packages, in topological order
. "${DIR}/projects.sh"
_projects=". ${PROJECTS}"
echo "Running on following projects: ${_projects}"
if [ "$(uname)" = "Darwin" ]; then export SEP=" "; else SEP=""; fi
for p in $_projects
do
  echo "Creating local version of ${p}"
  echo "$VERSION" > "${p}/VERSION"
  sed -i$SEP'' "s/^version = .*/version = \"$VERSION\"/" "$p/pyproject.toml"
done
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" kuflow-rest/kuflow_rest/__init__.py
sed -i$SEP'' "s/^VERSION.*/VERSION = \"$VERSION\"/" kuflow-rest/kuflow_rest/_generated/_version.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" kuflow-robotframework/KuFlow/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" kuflow-temporal-common/kuflow_temporal_common/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" kuflow-temporal-activity-kuflow/kuflow_temporal_activity_kuflow/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" kuflow-temporal-activity-robotframework/kuflow_temporal_activity_robotframework/__init__.py
# Example other package: sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" package-b/package_b/__init__.py
