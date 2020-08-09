#!/bin/sh
# sh -c "$(curl -H 'Cache-Control: no-cache' -LsSo- https://raw.githubusercontent.com/IgorAssuncao/system-config/master/start.sh)"

echo "This script automatically installs some tools and creates symlinks for you."
echo "All of these tools will be prompted to install:
    - QTile (A window manager written in python)
    - Kitty (A terminal emulator)
    - Kitty custom config
    - NeoVim (Newer version of vim)
    - Custom vimrc (vim config file)
    - Custom init.vim (nvim config file)
  "
echo "Do you want to continue?"
read -p "Please, answer (y/n): " -n 1 choice && \
  if [ $choice != "y" ]; then
    exit 1
  fi

echo "Downloading repo" && \
  git clone https://github.com/IgorAssuncao/system-config.git ~/system-config && \
  echo "Finished downloading repo"

echo "Install Qtile?"
read -p "Please, answer (y/n): " -n 1 choice && \
  if [ $choice != "y" ]; then
    exit 1
  else
    echo "Installing Qtile" && \
      sudo pacman -S qtile && \
      echo "Finished installed Qtile" && \
      echo "Creating qtile symlink" && \
      if [ -d "~/.config/qtile" ]; then
        echo "Renaming ~/.config/qtile to ~/.config/qtile.bkp"
        mv ~/.config/qtile ~/.config/qtile.bkp
      fi && \
        ln -s ~/system-config/.config/qtile/ ~/.config/qtile && \
        echo "Finished creating qtile symlink"
  fi

echo "Install Kitty?"
read -p "Please, answer (y/n): " -n 1 choice && \
  if [ $choice != "y" ]; then
    exit 1
  else
    echo "Installing kitty" && \
      sudo pacman -S kitty && \
      echo "Finished installing kitty"
      echo "Creating kitty symlink" && \
      if [ -d "~/.config/kitty" ]; then
        echo "Renaming ~/.config/kitty to ~/.config/kitty.bkp"
        mv ~/.config/kitty ~/.config/kitty.bkp
      fi && \
        ln -s ~/system-config/.config/kitty/ ~/.config/kitty && \
        echo "Finished creating kitty symlink"
  fi

echo "Install custom Kitty config?"
read -p "Please, answer (y/n): " -n 1 choice && \
  if [ $choice != "y" ]; then
    exit 1
  else
      echo "Creating kitty symlink" && \
      if [ -d "~/.config/kitty" ]; then
        echo "Renaming ~/.config/kitty to ~/.config/kitty.bkp"
        mv ~/.config/kitty ~/.config/kitty.bkp
      fi && \
        ln -s ~/system-config/.config/kitty/ ~/.config/kitty && \
        echo "Finished creating kitty symlink"
  fi

echo "Install NeoVim?"
read -p "Please, answer (y/n): " -n 1 choice && \
  if [ $choice != "y" ]; then
    exit 1
  else
    echo "Installing NeoVim" && \
      sudo pacman -S neovim && \
      echo "Finished installing NeoVim"
  fi

echo "Install custom vimrc?"
read -p "Please, answer (y/n): " -n 1 choice && \
  if [ $choice != "y" ]; then
    exit 1
  else
    if [ -a "~/.vimrc" ]; then
      echo "Renaming ~/.vimrc to ~/.vimrc.bkp"
      mv ~/.vimrc ~/.vimrc.bkp
    fi
    echo "Creating ~/.vimrc symlink" && \
      ln -s ~/system-config/.config/vim/vimrc ~/.vimrc
    echo "Creating ~/.vim/coc-settings synlink" && \
      ln -s ~/system-config/.config/vim/coc-settings.json ~/.vim/coc-settings.json
  fi

  echo "Install custom init.vim (nvim config file)?"
read -p "Please, answer (y/n): " -n 1 choice && \
  if [ $choice != "y" ]; then
    exit 1
  else
    if [ -d "~/.config/nvim" ]; then
      echo "Renaming ~/.config/nvim to ~/.config/nvim.bkp"
      mv ~/.config/nvim ~/.config/nvim.bkp
    fi
    echo "Creating ~/.config/nvim symlink" && \
      ln -s ~/system-config/.config/nvim ~/.config/nvim
  fi
