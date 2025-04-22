import os
from pathlib import Path
import subprocess

import yaml

from dotfile_manager.config import PROJECT_CONFIG_NAME


def run_script(script_path: Path, verbose: bool):
    """ Run a script as a subprocess. """
    assert script_path.exists(), script_path

    stdout = None if verbose else subprocess.PIPE
    stderr = None if verbose else subprocess.PIPE
    subprocess.run(script_path, check=True, stdout=stdout, stderr=stderr)


def force_symlink(source: Path, destination: Path):
    """ Create a symlink, similar to `ln -fs` in the shell. """
    assert source.exists(), source

    destination = destination.expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.unlink(missing_ok=True)

    os.symlink(source, destination)


class InvalidProjectError(Exception):
    """ Exception raised when a project is invalid. """


class Project:
    """ Class used to represent a dotfile project. """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.config_path = path / PROJECT_CONFIG_NAME
        self.name = self.path.name
        if not self.path.is_dir():
            raise InvalidProjectError(f"Project path {self.path}' is not a directory")
        if not self.config_path.exists():
            raise InvalidProjectError(f"Project config path {self.config_path}' does not exist")
        self.config = yaml.load(self.config_path.read_text(), Loader=yaml.FullLoader)
        self._is_installed = False

    def get_name(self) -> str:
        return self.name

    def get_requires(self) -> list[str]:
        return self.config.get('requires', [])

    def is_disabled(self) -> bool:
        return self.config.get('disable', False)

    def is_installed(self) -> bool:
        return self._is_installed

    def install(self, os_name: str, verbose: bool) -> None:
        print(f'Installing project {self.name} for {os_name}...')
        install_scripts = self.config.get(f'install_{os_name}', None)

        if not install_scripts:
            print('No configured install scripts found.')
            return

        for install_script in install_scripts:
            run_script(self.path / install_script, verbose=verbose)

        self._is_installed = True
        print(f'Successfully installed project {self.name} for {os_name}.')

    def create_symbolic_links(self) -> None:
        symlinks = self.config.get('symlinks', None)
        if not symlinks:
            print('No configured symlinks found.')
            return

        for source, destination in symlinks.items():
            force_symlink(self.path / source, Path(destination))
            print(f'Created symlink from {source} to {destination}.')

    def create_bin(self, destination_folder: Path) -> None:
        binaries = self.config.get('bin', None)
        if not binaries:
            print('No configured binaries found.')
            return

        for binary in binaries:
            binary_path = self.path / binary
            assert binary_path.exists(), binary_path

            # Use only binary_path.name s.t. we ignore the path if it is in a subfolder.
            destination = destination_folder / binary_path.name
            os.symlink(binary_path, destination)
            print(f'Created symlink from {binary_path} to {destination}.')

    def add_sources(self, output_file) -> None:
        source_files = self.config.get('source', None)
        if not source_files:
            print('No configured sourcing files found.')
            return

        for source_file in source_files:
            source_path = self.path / source_file
            assert source_path.exists(), source_path

            output_file.write(f'. {source_path}\n')
            print(f'Added {source_path} to sourced in {source_path}.')
