#!/bin/sh

set -e

python3 -m pip install twine
python3 setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
