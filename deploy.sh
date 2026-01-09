#!/bin/sh

set -e

rm -rf dist/
uv build
uv run twine check dist/*
uv run twine upload dist/*
