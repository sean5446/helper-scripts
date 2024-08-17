# Hyper-V Ubuntu 24.04 Installation

## Ubuntu Install
- Hyper-V: can use generation 2 hardware
- Hyper-V: disable secure boot
- During Ubuntu install: keep auto-login disabled at startup and add password

```sh
sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install xrdp vim 

sudo systemctl enable xrdp


vim /etc/xrdp/startwm.sh

(add to top of file)

export GNOME_SHELL_SESSION_MODE=ubuntu
export XDG_CURRENT_DESKTOP=ubuntu:GNOME

sudo apt-get install \
  build-essential python3-pip python3-venv htop git openssh-server zsh curl wget 

```
