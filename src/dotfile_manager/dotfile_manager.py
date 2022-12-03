from pathlib import Path
import argparse
import os

from dotfile_manager.cli import create_parser
from dotfile_manager.repo import Repo

def main():
    parser = create_parser()
    args = parser.parse_args()

    repo = Repo(args.dotfiles)
    if args.verb == 'install':
        if args.project:
            repo.install(args.project)
        else:
            repo.install_all()
        return

    if args.verb == 'setup':
        repo.setup_all()
        return

    print('Unknown verb, doing nothing.')
    return
