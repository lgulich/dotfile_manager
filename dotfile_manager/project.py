import os
from pathlib import Path
import subprocess
from typing import Any

import yaml
import typeguard

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


class ProjectConfig:
    """
    Class used to represent a project's configuration.

    This class automatically takes care of abstracting the configuration for a
    specific OS.
    """

    def __init__(self, config: dict[str, Any], os_name: str):
        self._config = config
        self._os_name = os_name

    def _get_config(self, key: str, expected_type: type) -> Any:
        all_values = self._config.get(key, [])

        # Return the os-specific values if they exist.
        if isinstance(all_values, dict) and self._os_name in all_values:
            os_values = all_values[self._os_name]
            typeguard.check_type(os_values, expected_type)
            return os_values

        # Check if the generic values can be returned or if they are for a
        # specific different os.
        try:
            # The type matches so we can return it.
            typeguard.check_type(all_values, expected_type)
            return all_values
        except typeguard.TypeCheckError:
            # The type does not match, so we will return the default value.
            return None

    def set_os_name(self, os_name: str) -> None:
        self._os_name = os_name

    def is_disabled(self) -> bool:
        return self._get_config('disable', bool) or False

    def get_requires(self) -> list[str]:
        return self._get_config('requires', list[str]) or []

    def get_install(self) -> list[str]:
        return self._get_config('install', list[str]) or []

    def get_symlinks(self) -> dict[str, str | list[str]]:
        return self._get_config('symlinks', dict[str, str | list[str]]) or {}

    def get_bin(self) -> list[str]:
        return self._get_config('bin', list[str]) or []

    def get_source(self) -> list[str]:
        return self._get_config('source', list[str]) or []

    @classmethod
    def load_from_path(cls, path: Path, os_name: str) -> 'ProjectConfig':
        config = yaml.load(path.read_text(), Loader=yaml.FullLoader)
        return cls(config, os_name)


class InvalidProjectError(Exception):
    """ Exception raised when a project is invalid. """


class Project:
    """ Class used to represent a dotfile project. """

    def __init__(self, path: Path, os_name: str) -> None:
        self._path = path
        self._os_name = os_name
        self._config_path = path / PROJECT_CONFIG_NAME
        if not self._path.is_dir():
            raise InvalidProjectError(f"Project path {self._path}' is not a directory")
        if not self._config_path.exists():
            raise InvalidProjectError(f"Project config path {self._config_path}' does not exist")

        self._config = ProjectConfig.load_from_path(self._config_path, os_name=self._os_name)
        self._name = self._path.name
        self._is_installed = False

    def set_os_name(self, os_name: str) -> None:
        self._os_name = os_name
        self._config.set_os_name(os_name)

    def get_name(self) -> str:
        return self._name

    def get_requires(self) -> list[str]:
        return self._config.get_requires()

    def is_disabled(self) -> bool:
        return self._config.is_disabled()

    def is_installed(self) -> bool:
        return self._is_installed

    def install(self, verbose: bool) -> None:
        print(f'Installing project {self._name} for {self._os_name}...')
        install_scripts = self._config.get_install()

        if not install_scripts:
            print('No configured install scripts found.')
            return

        for install_script in install_scripts:
            run_script(self._path / install_script, verbose=verbose)

        self._is_installed = True
        print(f'Successfully installed project {self._name} for {self._os_name}.')

    def create_symbolic_links(self) -> None:
        symlinks = self._config.get_symlinks()
        if not symlinks:
            print('No configured symlinks found.')
            return

        for source, destinations in symlinks.items():
            if not isinstance(destinations, list):
                destinations = [destinations]
            for destination in destinations:
                force_symlink(self._path / source, Path(destination))
                print(f'Created symlink from {source} to {destination}.')

    def create_bin(self, destination_folder: Path) -> None:
        binaries = self._config.get_bin()
        if not binaries:
            print('No configured binaries found.')
            return

        for binary in binaries:
            binary_path = self._path / binary
            assert binary_path.exists(), binary_path

            # Use only binary_path.name s.t. we ignore the path if it is in a subfolder.
            destination = destination_folder / binary_path.name
            os.symlink(binary_path, destination)
            print(f'Created symlink from {binary_path} to {destination}.')

    def add_sources(self, output_file) -> None:
        source_files = self._config.get_source()
        if not source_files:
            print('No configured sourcing files found.')
            return

        for source_file in source_files:
            source_path = self._path / source_file
            assert source_path.exists(), source_path

            output_file.write(f'. {source_path}\n')
            print(f'Added {source_path} to sourced in {source_path}.')
