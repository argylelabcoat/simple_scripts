#!/bin/sh
SIZE="$(du -b $1 | cut -f1)"

CMD="dd if=$1 | pv -s ${SIZE} | dd of=$2 bs=32M"
echo "${CMD}"
sudo sh -c "${CMD}"
