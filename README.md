# KuFlow SDK for Python

KuFlow SDK for Python

# Release

TODO:

To release, create a commit witha a message in python version format. Example: "v0.2.0"

For dev commits, tag as: "[\\.\\-]dev[\\.\\-]?.\*$".
Example: "0.3.1.dev"

# Develop

## To create all virtual environments.

`poetry_install.sh`

## If you want to run poetry update on all projects

`poetry_update.sh`

## To add a new package

Edit:
projects.sh: contains a list of all the poetry packages, in topological order

create_local_version.sh and pyproject.toml's

### If you add a dependency to one of the packages

If you add a dependency to one of the packages, you also want to update the upstream packages’ lock files in the mono repo.
`$./poetry_update.sh`

### Sharing development utilities

Some development utilities are repo wide dependencies. See the dev group of the root folder’s pyproject.toml. But production dependencies not exist in the root pyproject.toml.

Each package in the mono repo has all its dependencies, both production, and development. For example pytest to allows the IDE to use the version used in the package: `poetry run pytest`

### See more

Monorepo based in:

- https://gitlab.com/gerbenoostra/poetry-monorepo/
- https://gerben-oostra.medium.com/python-poetry-mono-repo-without-limitations-dd63b47dc6b8

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
