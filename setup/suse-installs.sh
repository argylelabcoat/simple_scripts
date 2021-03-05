#!/bin/sh

#################################################
## Source Control

sudo zypper install git mercurial subversion fossil

#################################################
## Development Patterns

sudo zypper in -t pattern devel_basis devel_C_C++ devel_python3

#################################################
## Development Libs / Tools

# I need openssl-devel for building starship.rs
# I need libnotify-devel for building tomboy-ng

sudo zypper install  openssl-devel libnotify-devel \
clang-tools \
lazarus anjuta anjuta-extras glade codelite gnome-builder \
neovim emacs \
scons ninja direnv


#################################################
## Commandline Tools

sudo zypper in fzf fd ripgrep bat the_silver_searcher

#################################################
## Containers / Tools

sudo zypper install podman buildah


#################################################
## BC-4

sudo rpm --import https://www.scootersoftware.com/RPM-GPG-KEY-scootersoftware
sudo zypper refresh
sudo zypper install https://www.scootersoftware.com/bcompare-4.3.7.25118.x86_64.rpm


#################################################
## Sublime Tools

sudo rpm -v --import https://download.sublimetext.com/sublimehq-rpm-pub.gpg
sudo zypper addrepo -g -f https://download.sublimetext.com/rpm/stable/x86_64/sublime-text.repo
sudo zypper install sublime-text sublime-merge

