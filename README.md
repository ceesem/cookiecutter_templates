# A set of cookiecutter files that I like that you may like too (*mutatis mutandis*).

All cookiecutters use `uv` for python environment management in a `pyproject.toml` file, alongside tools for maintenance and testing as needed.
The current toolset is:

0. Python application management: `pipx`. This is used to install various tools and is a variation of `pip` designed for command-line applications. Rather than installing in a specific environment, it installs in a separate environment and creates a symlink to the executable in the user's path. This is useful for tools that are used across multiple projects and need to be kept up to date. You will only need to install `pipx` once on your computer. See [pipx documentation](https://pipx.pypa.io/stable/) for instructions.
1. Environment Management : `uv` Recommended installation via `pipx install uv`. This will be used to manage the virtual environment for all projects, as well as building, publishing, and testing libraries.
2. Code Formatting : `ruff`. This will be installed within a virtual environment and is managed by `uv`, although it is also useful to install the VSCode extension for it if you use that editor.
3. Testing : `pytest`. This will be installed within a virtual environment and is managed by `uv`.
4. Documentation : `mkdocs-material` and `mkdocstrings`. This will be installed within a virtual environment and is managed by `uv`.
5. Version Management : `bump-my-version`. This will be installed within a virtual environment and is managed by `uv`.
6. Pre-commit format checking : `pre-commit` used with `ruff`. Pre-commit is run and/or installed and initialized by `uv` after cookiecutter creation. 
7. Version control: `git`.  If this is not installed, follow instructions online.
8. Automated testing and documnentation : GitHub Actions. This is handled via files in the `.github/workflows` directory and needs no additional installation.
9. Profiling via `scalene` and `pyinstrument`. These are installed and managed by `uv`. Use `poe profile-all` to profile cpu and memory with `scalene` and `poe profile` to profile cpu in an aesthetically nicer way with `pyinstrument`.
10. Script-aliasing: `poethepoet`. Recommended installation via `pipx install poethepoet`.
11. Large tasks: `python-task-queue`. This adds a simple way to build queues that can be distributed across many workers in the cloud.

In all cases, they are designed to make it easy to run notebooks within the directory of the new project via `vscode` with its ability to detect a local python interpreter at the root of the project under the `.venv` directory.
Each template is oriented toward different use case and have different needs and levels of opinion and automation. The current templates are:

* **uv-library** : Creating a python library that will be published to PyPI, with testing, documentation, and version management using all of the above tools. Stubs are created for documentation and testing, and the library is set up to be published to PyPI. GitHub actions will run testing against a matrix of python versions and publish the documentation to GitHub pages.
* **uv-analysis** : This is designed for a longer term analysis project where data, plots, and notebooks will be saved. It will be checked into version control, but actual pypi releases are not expected. 
* **uv-oneoff** : This is designed for a one-off analysis or notebook that will not be checked into version control. It is designed to be run in a local environment and not shared with others. It does include a number of basic packages that I use for data analysis and visualization as well as interaction with CAVE. Profiling is not set up here.
* **uv-task** : This is designed for a queue/worker task deployed through `python-task-queue`. It is designed to help create, distribute, and deploy tasks and workers using Google Kubernetes Engine.

To use any of these cookiecutters, you will need to have `cookiecutter` installed. This can be done via `pipx install cookiecutter`.
To allow you to use these templates from anywhere, you can symlink them to the `~/.cookiecutters` directory.
This can be done in the terminal by navigating to the base of this directory and running:

```bash
ln -s uv-library ~/.cookiecutters/uv-library
ln -s uv-analysis ~/.cookiecutters/uv-analysis
ln -s uv-oneoff ~/.cookiecutters/uv-oneoff
ln -s uv-task ~/.cookiecutters/uv-task
```

Then, to create a new project, navigate to the directory where you want the project and simply run `cookiecutter uv-library` (or whatever template you want to use).
