#!/bin/sh

source $HOME/.cargo/env
if ! command -v cargo %> /dev/null
then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  source $HOME/.cargo/env
fi

cargo install starship