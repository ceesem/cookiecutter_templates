# {{ cookiecutter.project_slug }} Scratch Workspace

This directory provides a scratch workspace for developing and testing the parent library `{{ cookiecutter.project_slug }}`.

The library is installed as an editable dependency, so changes to the source code are immediately reflected here.

## Usage

```bash
cd scratch
uv sync
```

And start your notebook as needed.
Add any additional dependencies you need for exploration or testing.
This directory is git-ignored and can be used freely without affecting the main repository.
