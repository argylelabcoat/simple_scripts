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
asdf install direnv 2.20.0
asdf global  direnv 2.20.0

mkdir -p $HOME/.config/direnv

cat >> $HOME/.config/direnv/direnvrc <<'EOF'
 source "$(asdf direnv hook asdf)" 
EOF

## MESON
asdf plugin-add meson https://github.com/asdf-community/asdf-meson.git

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

