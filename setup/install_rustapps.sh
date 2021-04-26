#!/bin/sh

source $HOME/.cargo/env
if ! command -v cargo %> /dev/null
then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  source $HOME/.cargo/env
  rustup update stable
fi

cargo install starship

cargo install lsd

cargo install --git https://github.com/ClementTsang/bottom
