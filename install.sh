#!/bin/bash

set -e

script_path=$(dirname "$0")
python3 -m pip install "${script_path}" --upgrade
