#!/bin/bash
git init
uv sync
uvx pre-commit install
chmod +x .bmv-post-commit.sh