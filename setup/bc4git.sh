#!/bin/sh
git config --global diff.tool bc
git config --global difftool.prompt false
git config --global difftool.bc trustExitCode true

git config --global merge.tool bc
git config --global mergetool.bc trustExitCode true