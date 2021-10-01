import argparse

from dotfile_manager.core import *
from dotfile_manager.version import __version__

def main():
    parser = argparse.ArgumentParser(
            description='Tool for managing dotfiles for linux and macos.')
    parser.add_argument('-d','--dotfiles',
            type=str, default='',
            help='Path to the dotfiles repository')
    parser.add_argument('-v',
            '--version',
            action='version',
            version=__version__,
            help='Print the version')

    verb_parser = parser.add_subparsers(dest='verb')
    verb_parser.required = True

    setup_parser = verb_parser.add_parser('setup', help='Setup dotfiles')
    install_parser = verb_parser.add_parser('install', help='Install dependencies of dotfiles')

    args = parser.parse_args()

    # If dotfiles path is not set via CLI we fallback to env variable and then
    # current working directory.
    dotfiles_path = args.dotfiles
    if dotfiles_path == '':
        if DOTFILES_PATH_ENV_VARIABLE in os.environ:
            dotfiles_path = Path(os.environ[DOTFILES_PATH_ENV_VARIABLE])
        else:
            dotfiles_path = Path(os.getcwd())

    if args.verb == 'install':
        install_dependencies(dotfiles_path)
        return

    if args.verb == 'setup':
        create_symbolic_links(dotfiles_path)
        create_bin(dotfiles_path)
        create_sources(dotfiles_path)
        return
