#!/usr/bin/env bash


export NVM_DIR="$HOME/.nvm"
if ! [ -d $NVM_DIR ]; then
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
fi
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

nvm install --lts
nvm use --lts
