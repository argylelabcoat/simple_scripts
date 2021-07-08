#!/bin/sh

#################################################
## Source Control

sudo zypper install -y git git-lfs mercurial subversion fossil

#################################################
## Development Patterns

sudo zypper in -y -t pattern devel_basis devel_C_C++ devel_python3

#################################################
## Development Libs / Tools

# I need openssl-devel for building starship.rs
# I need libnotify-devel for building tomboy-ng

sudo zypper in -y openssl-devel libnotify-devel \
clang-tools \
lazarus anjuta anjuta-extras glade codelite gnome-builder \
cmake scons ninja direnv \
clang12 clang-tools lldb12 \
libc++1 libc++abi-devel libc++abi1 libc++-devel \

#################################################
## Embedded Development 

sudo zypper in -y sdcc sdcc-doc avr-libc avrdude uisp \
  cross-avr-binutils cross-avr-gcc11 cross-arm-none-gcc11 \
  cross-arm-none-gcc11-bootstrap cross-arm-binutils \
  openocd cc-tool

#################################################
## Compression Tools
sudo zypper in -y zip unzip zstd bzip2 xz

#################################################
## Commandline Tools

sudo zypper in -y fzf fd ripgrep bat the_silver_searcher \
  bc lzop maim asciinema ranger tmux screen calcurse \
  nmap password-store dirmngr xclip

#################################################
## Editor Tools

sudo zypper in -y ShellCheck editorconfig MultiMarkdown-6 \
  neovim emacs

#################################################
## Graphics Tools 

sudo zypper in -y inkscape gimp gimp-ufraw ImageMagick \
  blender krita goxel

# wishlist
# dust3d


#################################################
## CAD Tools 

sudo zypper in -y openscad FreeCAD librecad leocad

#################################################
## Electronics Tools 

sudo zypper in -y kicad kicad-packages3D \
  fritzing fritzing-parts \
  pcb 

#################################################
## Containers / Tools

sudo zypper install -y podman buildah


#################################################
## BC-4

sudo rpm --import https://www.scootersoftware.com/RPM-GPG-KEY-scootersoftware
sudo zypper refresh
sudo zypper install -y https://www.scootersoftware.com/bcompare-4.3.7.25118.x86_64.rpm


#################################################
## Sublime Tools

sudo rpm -v --import https://download.sublimetext.com/sublimehq-rpm-pub.gpg
sudo zypper addrepo -g -f https://download.sublimetext.com/rpm/stable/x86_64/sublime-text.repo
sudo zypper install -y sublime-text sublime-merge

