# Developing kuflow-sdk-python

This doc is intended for contributors to `kuflow-sdk-python` repository. See also the contribution guide for each module in this repository.

## Development Environment

Main tools:

- Python 3.8+
- Poetry
- Black (code formatter)
- Flake 8 (linter)
- PyTest

We strongly recommend the use of python [virtual environments](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments) to work with.

## Develop

#### To create monorepo virtual environment

```shell
poetry install
```

#### Dependencies

If a new dependency has been added to any of the poetry file, run the helper script. You can use poetry for dependency management but remember that this is a monorepo, see in which module you want to add it. However, the most convenient way is to update the appropriate pyproject.toml file and update all environments. To do this you must run:

```bash
./scripts/poetry_run_on_each.sh update
```

Remember that this command gets the latest versions of the dependencies and to update the poetry.lock file.

#### Sharing development utilities

Some development utilities are repo wide dependencies. See the dev group of the root folder’s pyproject.toml. But production dependencies not exist in the root pyproject.toml.

Each package in the mono repo has all its dependencies, both production, and development. For example pytest to allows the IDE to use the version used in the package: `poetry run pytest`

#### Adding a new module

Update `scripts/projects.sh` to list all the poetry packages in the mono repo. The list should be in topological order: it should list a package’s dependencies before the depending package.

Update `scripts/create_local_version.sh` with a new `sed` expression with the new module

#### Versioning

We use [PEP 440 - Version Identification and Dependency Specification](https://peps.python.org/pep-0440/) to set the right version of the project. As a monorepo, all modules will share the same version.

To do this, always develop with a development version tag (the finished ones with a development release segment), e.g.: **0.1.0.dev0**.

How is the version set?

Edit `scripts/create_local_version.sh` and set in the variable `VERSION`

Then, execute

```bash
./scripts/create_local_version.sh
```
After that, execute a lock in each submodule:

```bash
./scripts/poetry_run_on_each.sh lock
```

Or without update dependencies:
```bash
./scripts/poetry_run_on_each.sh lock --no-update
```

### See more

Monorepo based in:

- https://gitlab.com/gerbenoostra/poetry-monorepo/
- https://gerben-oostra.medium.com/python-poetry-mono-repo-without-limitations-dd63b47dc6b8
