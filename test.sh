#!/bin/bash

set -e

SCRIPT_PATH=$(dirname "$0")
python3 -m pytest -v "${SCRIPT_PATH}"
