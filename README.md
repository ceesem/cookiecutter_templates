# A set of cookiecutter files for my own use.

All cookiecutters use `uv` for python environment management in a `pyproject.toml` file, alongside tools for maintenance and testing as needed.
The current toolset is:

0. Python application management: `pipx`. This is used to install various tools and is a variation of `pip` designed for command-line applications. Rather than installing in a specific environment, it installs in a separate environment and creates a symlink to the executable in the user's path. This is useful for tools that are used across multiple projects and need to be kept up to date. You will only need to install `pipx` once on your computer. See [pipx documentation](https://pipx.pypa.io/stable/) for instructions.
1. Code Formatting : `ruff`. This will be installed within a virtual environment and is managed by `uv`, although it is also useful to install the VSCode extension for it if you use that editor.
2. Testing : `pytest`. This will be installed within a virtual environment and is managed by `uv`.
3. Documentation : `mkdocs-material` and `mkdocstrings`. This will be installed within a virtual environment and is managed by `uv`.
4. Version Management : `bump-my-version`. This will be installed within a virtual environment and is managed by `uv`.
5. Script-aliasing: `poethepoet`. Recommended installation via `pipx install poethepoet`.
6. Environment Management : `uv` Recommended installation via `pipx install uv`. This will be used to manage the virtual environment for all projects, as well as building, publishing, and testing libraries.
7. Pre-commit format checking : `pre-commit` used with `ruff`. Pre-commit is run and/or installed and initialized by `uv` after cookiecutter creation. 
8. Version control: `git`.  If this is not installed, follow instructions online.
9. Automated testing and documnentation : GitHub Actions. This is handled via files in the `.github/workflows` directory and needs no additional installation.
10. Profiling via `scalene` and `pyinstrument`. These are installed and managed by `uv`. Use `poe profile-all` to profile cpu and memory with `scalene` and `poe profile` to profile cpu in an aesthetically nicer way with `pyinstrument`.

In all cases, they are designed to make it easy to run notebooks within the directory of the new project via `vscode` with its ability to detect a local python interpreter at the root of the project under the `.venv` directory.
Each template is oriented toward different use case and have different needs and levels of opinion and automation. The current templates are:

* **uv-library** : Creating a python library that will be published to PyPI, with testing, documentation, and version management using all of the above tools. Stubs are created for documentation and testing, and the library is set up to be published to PyPI. GitHub actions will run testing against a matrix of python versions and publish the documentation to GitHub pages.
* **uv-analysis** : This is designed for a longer term analysis project where data, plots, and notebooks will be saved. It will be checked into version control, but actual pypi releases are not expected. 
* **uv-oneoff** : This is designed for a one-off analysis or notebook that will not be checked into version control. It is designed to be run in a local environment and not shared with others. It does include a number of basic packages that I use for data analysis and visualization as well as interaction with CAVE. Profiling is not set up here.
