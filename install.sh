#!/bin/bash

set -e

script_path=$(dirname "$0")
python3 -m pip uninstall dotfile_manager -y || true
python3 -m pip install "${script_path}" --upgrade
