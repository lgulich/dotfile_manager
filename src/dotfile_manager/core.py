import os
import shutil
from pathlib import Path
from datetime import datetime
import subprocess
import platform

import yaml

DOTFILES_PATH_ENV_VARIABLE = 'DOTFILES'
BIN_PATH = 'generated/bin/'
SOURCE_FILE_PATH = 'generated/sources.zsh'
PROJECT_CONFIG_NAME = 'dotfile_manager.yaml'


def get_os_name() -> str:
    platform_name = platform.system()
    # TODO(lgulich): Find way to also determine linux distro.
    if platform_name == 'Linux':
        return 'ubuntu'
    if platform_name == 'Darwin':
        return 'macos'
    raise


class DotfileProject:

    def __init__(self, path: Path):
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
                is_disabled = yaml.load(file, Loader=yaml.FullLoader)[f'disable']
                return is_disabled
            except KeyError:
                return False

    def install(self):
        os = get_os_name()
        self.install_for_os(os)
        print(f'Successfully installed project {self.name}.')

    def install_for_os(self, os):
        with open(self.path / PROJECT_CONFIG_NAME) as file:
            try:
                install_scripts = yaml.load(file, Loader=yaml.FullLoader)[f'install_{os}']
            except KeyError:
                return

            for install_script in install_scripts:
                script = self.path / install_script
                assert script.exists(), script
                subprocess.run(script)

    def create_symbolic_links(self):
        with open(self.path / PROJECT_CONFIG_NAME) as file:
            try:
                symlinks = yaml.load(file, Loader=yaml.FullLoader)['symlinks']
            except KeyError:
                return

            for source, destination in symlinks.items():
                source_path = self.path / source
                assert source_path.exists(), source_path

                destination_path = Path(destination).expanduser()
                destination_path.parent.mkdir(parents=True, exist_ok=True)
                destination_path.unlink(missing_ok=True)

                os.symlink(source_path, destination_path)
                print(f'Created symlink from {source_path} to '
                        f'{destination_path}.')

    def create_bin(self, destination_folder):
        with open(self.path / PROJECT_CONFIG_NAME) as file:
            try:
                binaries = yaml.load(file, Loader=yaml.FullLoader)['bin']
            except KeyError:
                return

            for binary in binaries:
                binary_path = self.path / binary
                assert binary_path.exists(), binary_path

                destination = destination_folder / binary
                os.symlink(binary_path, destination)
                print(f'Created symlink from {binary_path} to {destination}.')

    def create_sources(self, output_file):
        with open(self.path / PROJECT_CONFIG_NAME) as file:
            try:
                source_files = yaml.load(file, Loader=yaml.FullLoader)['source']
            except KeyError:
                return

            for source_file in source_files:
                source_path = self.path / source_file
                assert source_path.exists(), source_path

                output_file.write(f'source {source_path}\n')
                print(f'Added {source_path} to sourcing script.')


def install(dotfiles: Path) -> None:
    for child in dotfiles.iterdir():
        project = DotfileProject(child)
        if not project.is_valid_project():
            continue
        if project.is_disabled():
            print(f'Project {project.get_name()} is disabled - Skipping.')
            continue
        project.install()
    print('Successfully installed all projects.')


def create_symbolic_links(dotfiles: Path) -> None:
    for child in dotfiles.iterdir():
        project = DotfileProject(child)
        if not project.is_valid_project():
            continue
        if project.is_disabled():
            print(f'Project {project.get_name()} is disabled - Skipping.')
            continue
        project.create_symbolic_links()
    print('Successfully setup symlinks to all dotfiles.')


def create_bin(dotfiles: Path) -> None:
    destination = Path(dotfiles / BIN_PATH)
    shutil.rmtree(destination, ignore_errors=True)
    destination.mkdir(parents=True)
    for child in dotfiles.iterdir():
        project = DotfileProject(child)
        if not project.is_valid_project():
            continue
        if project.is_disabled():
            print(f'Project {project.get_name()} is disabled - Skipping.')
            continue
        project.create_bin(destination)
    print('Successfully setup symlinks to all binaries.')


def create_sources(dotfiles: Path) -> None:
    destination = Path(dotfiles / SOURCE_FILE_PATH)
    destination.unlink(missing_ok=True)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with open(destination, 'a') as output_file:
        output_file.write(f'# Autogenerated on {datetime.now()}.\n')
        output_file.write(f'# shellcheck shell=zsh\n\n')

        for child in dotfiles.iterdir():
            project = DotfileProject(child)
            if not project.is_valid_project():
                continue
            if project.is_disabled():
                print(f'Project {project.get_name()} is disabled - Skipping.')
                continue
            project.create_sources(output_file)
    print(f'Successfully created sourcing script at {destination}.')
