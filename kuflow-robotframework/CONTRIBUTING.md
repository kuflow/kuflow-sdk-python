# Developing kuflow-robotframework

This doc is intended for contributors to `kuflow-robotframework`

## Development Environment

- Python 3.8+
- Poetry
- Black (code formatter)
- Flake 8 (linter)
- PyTest

## Build

### Formatter

To format code:

```bash
poetry run black
# Or
npm run black
```

### RobotFramework keywords

The keywords of RobotFramework library are in [keywords.py](KuFlow/keywords.py) file. Please make sure they are properly documented.

## Test

Run all the tests with:

```bash
poetry run pytest
```
