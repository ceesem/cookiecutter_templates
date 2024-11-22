#!/bin/zsh
git init
uv venv --seed
uv sync
uvx pre-commit install