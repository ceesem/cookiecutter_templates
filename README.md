# A set of cookiecutter files for my own use.

All cookiecutters use `uv` for python environment management in a `pyproject.toml` file, alongside tools for maintenance and testing as needed.
The current toolset is:

1. Code Formatting : `ruff`
2. Testing : `pytest`
3. Documentation : `mkdocs-material` and `mkdocstrings`.
4. Version Management : `bump-my-version`
5. Script-aliasing: `poethepoet`
6. Environment Management : `uv`
7. Pre-commit format checking : `pre-commit` used with `ruff`.
8. Version control: `git`
9. Automated testing and documnentation : GitHub Actions.

In all cases, they are designed to make it easy to run notebooks within the directory of the new project via `vscode` with its ability to detect a local python interpreter at the root of the project under the `.venv` directory.
Each template is oriented toward different use case and have different needs and levels of opinion and automation. The current templates are:

* **uv-library** : Creating a python library that will be published to PyPI, with testing, documentation, and version management using all of the above tools. Stubs are created for documentation and testing, and the library is set up to be published to PyPI. GitHub actions will run testing against a matrix of python versions and publish the documentation to GitHub pages.
* **uv-analysis** : This is designed for a longer term analysis project where data, plots, and notebooks will be saved. It will be checked into version control, but actual pypi releases are not expected. 
* **uv-oneoff** : This is designed for a one-off analysis or notebook that will not be checked into version control. It is designed to be run in a local environment and not shared with others. It does include a number of basic packages that I use for data analysis and visualization as well as interaction with CAVE.

