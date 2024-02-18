# Dotfile Manager [![Python package](https://github.com/lgulich/dotfile_manager/actions/workflows/ci.yml/badge.svg)](https://github.com/lgulich/dotfile_manager/actions/workflows/ci.yml)

A dotfile manager to easily reuse configurations between linux and macOS.

## Installation

```
pip install dotfile-manager
```

## Usage

* Make sure your dotfiles are organized as described below.

* `cd` into your dotfiles repo.

* Installing the dotfiles: This will install all the necessary dependencies for
  your dotfiles.

  ```sh
  dotfile_manager install
  ```

* Setting up the dotfiles: This will set up symbolic links for the config files,
  symlink binaries and create a script to source everything.

  ```sh
  dotfile_manager setup
  ```

## Organize your dotfiles for use with the dotfile manager

A minimal example of how to organize your dotfiles can be seen [here](test/test_data/dotfiles_repo),
a real-life example [here](https://github.com/lgulich/dotfiles).

The dotfiles are organised by project, where each project has its own top-level
folder. A project has to contain a file `dotfile_manager.yaml` which configures the
dotfile manager. It is setup as follows:

```yaml
install_macos:
  - install_macos.sh

install_ubuntu:
  - install_ubuntu.sh

symlinks:
  zshrc.zsh: ~/.zshrc

bin:
  - do_something.sh

source:
  - aliases.sh
  - helpers.sh

disable: False
```

The entries of `install_macos` configure what scripts are used to install this project on macos.
`install_ubuntu` does the same for ubuntu. Multiple scripts can be provided and they are executed in
the order as specified in the yaml file.

The entries of `symlinks` configure where the files will be symlinked to, the key is the path of the
file inside the topic folder, the value is the global path where the file will be symlinked to. Use
this to setup configuration files that need to be at a specific location (for example `.bashrc`
which has to be in `~/`). It is possible to use `~` to specify the path of files that need to go to
a user's ``$HOME` folder.

The entries of `bin` will be symlinked to `${DOTFILES}/generated/bin/`. Add the latter to your
`$PATH` to easily execute these binaries from everywhere.

The entries of `source` will be added to a script in
`${DOTFILES}/generated/sources.zsh`, such that you only have to source this file
instead of sourcing all files individually.

Lastly `disable` can be used to disable a dotfile project. If this is set to true this project will
be skipped during installation and setup.

All these entries are optional. If you don't need them you can simply omit them.

## Advanced

To work correctly the dotfile manager needs to know where the repo with all your
dotfiles is stored. Thus you need to run the `dotfile_manager [install|setup]`
command from the directory where your dotfiles are stored. If you want to be
able to run the dotfile manager from anywhere there are two options:

* Use a command line argument:
  ```sh
  dotfile_manager -d <path/to/dotfiles/> install
  ```
* Use an environment variable:
  ```sh
  export DOTFILES=<path/to/dotfiles>
  dotfile_manager install
  ```
