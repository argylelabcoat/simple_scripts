#!/bin/sh

# Install yay
sudo pacman -S yay
# Dev Base
sudo pacman -S base-devel
# Pkgs
sudo pacman -S \
lsd starship nnn ranger bat fzf fd ripgrep the_silver_searcher asciinema \
procs skim uncrustify ytop \
neovim nedit zile mg \
global ctags editorconfig-core-c \
clang llvm lld rustup elixir \
meson meson-tools cmake ninja \
cppcheck splint \
xz zstd gzip bzip2 zip unzip lzop \
thunar thunar-archive-plugin thunar-media-tags-plugin thunar-volman \
git mercurial subversion fossil \
zathura zathura-cb zathura-djvu zathura-pdf-mupdf zathura-ps \
maim rofi alacritty

yay -S \
emacs-native-comp-git-enhanced \
asdf-vm direnv \
infer-bin cpplint shellcheck-bin
