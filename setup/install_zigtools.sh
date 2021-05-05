#!/bin/bash
set -e

mkdir /tmp/zigtools && cd /tmp/zigtools

git clone --recurse-submodules https://github.com/zigtools/zls
cd zls
zig build -Drelease-safe
sudo cp ./zig-cache/bin/zls /usr/local/zig/current/
zls config

