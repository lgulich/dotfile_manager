import os
from pathlib import Path
import subprocess

import yaml

from dotfile_manager.config import PROJECT_CONFIG_NAME


class Project:

    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = self.path.name

    def get_name(self) -> str:
        return self.name

    def is_valid_project(self) -> bool:
        return self.path.is_dir() and (self.path / PROJECT_CONFIG_NAME).exists()

    def is_disabled(self) -> bool:
        with open(self.path / PROJECT_CONFIG_NAME) as file:
            try:
                # This key is optional. If not specified we assume the project to be enabled.
                is_disabled = yaml.load(file, Loader=yaml.FullLoader)['disable']
                return is_disabled
            except KeyError:
                return False

    def install(self, os) -> None:
        with open(self.path / PROJECT_CONFIG_NAME) as file:
            try:
                install_scripts = yaml.load(file, Loader=yaml.FullLoader)[f'install_{os}']
            except KeyError:
                return

            for install_script in install_scripts:
                script = self.path / install_script
                assert script.exists(), script
                subprocess.run(script)

        print(f'Successfully installed project {self.name} for {os}.')

    def create_symbolic_links(self) -> None:
        with open(self.path / PROJECT_CONFIG_NAME) as file:
            try:
                symlinks = yaml.load(file, Loader=yaml.FullLoader)['symlinks']
            except KeyError:
                print('No configured symlinks found.')
                return

            for source, destination in symlinks.items():
                source_path = self.path / source
                assert source_path.exists(), source_path

                destination_path = Path(destination).expanduser()
                destination_path.parent.mkdir(parents=True, exist_ok=True)
                destination_path.unlink(missing_ok=True)

                os.symlink(source_path, destination_path)
                print(f'Created symlink from {source_path} to {destination_path}.')

    def create_bin(self, destination_folder: Path) -> None:
        with open(self.path / PROJECT_CONFIG_NAME) as file:
            try:
                binaries = yaml.load(file, Loader=yaml.FullLoader)['bin']
            except KeyError:
                print('No configured binaries found.')
                return

            for binary in binaries:
                binary_path = self.path / binary
                assert binary_path.exists(), binary_path

                destination = destination_folder / binary
                os.symlink(binary_path, destination)
                print(f'Created symlink from {binary_path} to {destination}.')

    def add_sources(self, output_file) -> None:
        with open(self.path / PROJECT_CONFIG_NAME) as file:
            try:
                source_files = yaml.load(file, Loader=yaml.FullLoader)['source']
            except KeyError:
                print('No configured sourcing files found.')
                return

            for source_file in source_files:
                source_path = self.path / source_file
                assert source_path.exists(), source_path

                output_file.write(f'. {source_path}\n')
                print(f'Added {source_path} to sourced in {source_path}.')
