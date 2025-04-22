#!/bin/sh

set -e

# Check dependencies are installed:
if [ ! -f topic_d_install_ubuntu.txt ]; then
  echo "Topic D was not yet installed, but is required."
  exit 1
fi

echo "Installing topic a for ubuntu."
touch topic_a_install_ubuntu.txt
