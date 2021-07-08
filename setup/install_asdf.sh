#!/bin/bash

cd $HOME

git clone https://github.com/asdf-vm/asdf.git ~/.asdf
cd ~/.asdf
git checkout "$(git describe --abbrev=0 --tags)"

. $HOME/.asdf/asdf.sh
. $HOME/.asdf/completions/asdf.bash


#### PLUGINS

## DIRENV
asdf plugin-add direnv
asdf install direnv 2.28.0
asdf global  direnv 2.28.0

mkdir -p $HOME/.config/direnv

cat >> $HOME/.config/direnv/direnvrc <<'EOF'
source "$(asdf direnv hook asdf)" 

layout_poetry() {
  if [[ ! -f pyproject.toml ]]; then
    log_error 'No pyproject.toml found. Use `poetry new` or `poetry init` to create one first.'
    exit 2
  fi

  # create venv if it doesn't exist
  poetry run true

  export VIRTUAL_ENV=$(poetry env info --path)
  export POETRY_ACTIVE=1
  PATH_add "$VIRTUAL_ENV/bin"
}
EOF

cat >> $HOME/.tool-versions <<'EOF'
direnv 2.28.0
rust stable
go 1.16.4
nodejs lts-erbium
starship 0.54.0
lsd 0.20.1
EOF

## MESON
asdf plugin-add meson https://github.com/asdf-community/asdf-meson.git

## CMake
asdf plugin-add cmake

## Ninja
asdf plugin-add ninja

## RUST
asdf plugin-add rust https://github.com/code-lever/asdf-rust.git

## Poetry
asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git

## Zig
asdf plugin-add zig https://github.com/cheetah/asdf-zig.git

## Elixir
asdf plugin-add elixir https://github.com/asdf-vm/asdf-elixir.git

## Go
asdf plugin-add golang https://github.com/kennyp/asdf-golang.git

## NodeJS
asdf plugin-add nodejs

## Yarn
asdf plugin-add yarn

## Starship
asdf plugin-add starship

## My LSD Plugin
asdf plugin add lsd https://github.com/argylelabcoat/asdf-lsd

## flutter
asdf plugin add flutter https://github.com/argylelabcoat/asdf-flutter
