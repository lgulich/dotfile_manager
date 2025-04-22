#!/bin/sh

set -e

python3 -m pip install pipx --break-system-packages
python3 -m pipx install build twine

rm -rf dist/
python3 -m pipx run build --sdist --wheel .
python3 -m pipx run twine check dist/*
python3 -m pipx run twine upload dist/*
