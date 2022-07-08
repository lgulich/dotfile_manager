# Dotfiles [![CI](https://github.com/lgulich/dotfile_manager/actions/workflows/test.yml/badge.svg)](https://github.com/lgulich/dotfile_manager/actions/workflows/test.yml)

A dotfile manager to easily reuse configurations between linux and macOS.

## Installation

```
pip install dotfile-manager
```

## Usage

* Make sure your dotfiles are organized as described below.

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

The dotfiles are organised by project, where each project has its own top-level
folder. A project may contain a file `dotfile_manager.yaml` which configures the
dotfile manager. It is setup as follows:

```yaml
symlink:
  zshrc.zsh: ~/.zshrc

bin:
  - do_something.sh

source:
  - aliases.sh
  - helpers.sh
```

The entries of `symlink` configures where the files will be symlinked to, the
key is the path of the file inside the topic folder, the value is the global
path where the file will be symlinked to.

The entries of `bin` will be symlinked to `${DOTFILES}/generated/bin/`. Add this
folder to your path to easily access these binaries.

The entries of `source` will be added to a script in
`${DOTFILES}/generated/sources.zsh`, such that you only have to source this file
instead of sourcing all files individually.

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
