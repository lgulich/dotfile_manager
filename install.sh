#!/bin/bash

set -e

SCRIPT_PATH=$(dirname "$0")
python3.8 -m pip install "${SCRIPT_PATH}" --upgrade
