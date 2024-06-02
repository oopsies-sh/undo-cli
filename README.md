# Setup Instructions

## 1. Install Poetry

If you haven't already installed Poetry, you can install it by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

## 2. Install Dependencies

Navigate to your project directory and install the dependencies:

```bash
cd /path/to/undo-cli
poetry install
```

## 3. Build Package and Install

After building the package, you can install it globally using pipx or make:
    
```bash
# Make
make install

# pipx
pipx install dist/undo_cli-0.1.0-py3-none-any.whl
```

## 4. Run 
Running `oopsies show` in the cli should now yield the git log.



