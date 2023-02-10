# KuFlow SDK for Python

KuFlow SDK for Python

# Release

TODO:

To release, create a commit witha a message in python version format. Example: "v0.2.0"

For dev commits, tag as: "[\\.\\-]dev[\\.\\-]?.*$".
Exa,ple: "0.3.1.dev"



# Develop

## To add a new package

Edit:
projects.sh: contains a list of all the poetry packages, in topological order

create_local_version.sh and pyproject.toml's




Monorepo based in https://gitlab.com/gerbenoostra/poetry-monorepo/

## Usage
To create the poetry virtual environments:
```shell
scripts/poetry_install.sh
```
It might update the `poetry.lock` files, which is mainly usefull when running on new architectures.

If a new dependency has been added to any of the poetry file, run the helper script to update all lock files:
```shell
scripts/poetry_update.sh
```
It by design will update all `poetry.lock` files, such that updated transitive dependencies are correct.
It might also update other transitive dependencies to latest versions.

On the build server, one can determine the actual local semver version of the current checkout, and update all version numbers in the codebase:
```shell
poetry run scripts/create_local_version.sh
```
Note that this changes the `pyproject.toml` files and all python files containing versions, which **should not be committed** to git.

To build all the wheels, run
```shell
scripts/poetry_build.sh
```
Note that this changes the `pyproject.toml` files with changes that **should not be committed** to git.

Alternatively, to not have to modify `pyproject.toml` files, one can first build the packages.
Then, we need to modify the dependencies in the wheel & tar.gz artifacts.
This is done as follows (without invoking `poetry_build.sh`):
```shell
cd package-b
poetry build
../scripts/replace_path_deps.sh
```