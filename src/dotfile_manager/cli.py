from pathlib import Path
import argparse
import os

from dotfile_manager.repo import Repo
from dotfile_manager.version import __version__
from dotfile_manager.config import DOTFILES_PATH_ENV_VARIABLE


def get_default_dotfiles_path() -> Path:
    """
    Get the default dotfiles path. This is the env variable if set, else the current working
    directory.
    """
    if DOTFILES_PATH_ENV_VARIABLE in os.environ:
        return Path(os.environ[DOTFILES_PATH_ENV_VARIABLE])

    return Path(os.getcwd())


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Tool for managing dotfiles for linux and macos.')
    parser.add_argument('-d',
                        '--dotfiles',
                        type=Path,
                        default=get_default_dotfiles_path(),
                        help='Path to the dotfiles repository')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version=__version__,
                        help='Print the version')

    verb_parser = parser.add_subparsers(dest='verb')
    verb_parser.required = True

    install_parser = verb_parser.add_parser('install', help='Install dependencies of dotfiles')
    install_parser.add_argument('project', type=str, nargs='?', help='Name of dotfile project that will be installed')

    _ = verb_parser.add_parser('setup', help='Setup dotfiles')
    return parser
