#!/bin/bash
#
# SocietySpy: Open Source
# License: General Public License
# System: GNU/linux
# Date: 22-04-2022
#
# Facebook: https://www.facebook.com/whitehacks00
# TikTok: https://tiktok.com/@whitehacks00
# Telegram: https://t.me/whitehacks00
# GitHub: https://github.com/Darkmux
#
# This tool was created in honor of @thelinuxchoice.
#
# ==============================================
#                   Variables
# ==============================================
operatingSystem=$(uname -o)
deviceArchitecture=$(uname -m)
showPath=$(pwd)
showDay=$(date +"%d")
showMonth=$(date +"%m")
showYear=$(date +"%Y")
spy="/data/data/com.termux/files/home/societyspy"
settings="/data/data/com.termux/files/home/societyspy/settings"
style="/data/data/com.termux/files/home/societyspy/settings/style"
execute="/data/data/com.termux/files/home/societyspy/settings/exec"
intools="/data/data/com.termux/files/home/societyspy/settings/intools"
rmtools="/data/data/com.termux/files/home/societyspy/settings/rmtools"
home="/data/data/com.termux/files/home"
usr="/data/data/com.termux/files/usr"
etc="/data/data/com.termux/files/usr/etc"
bin="/data/data/com.termux/files/usr/bin"
opt="/data/data/com.termux/files/usr/opt"
share="/data/data/com.termux/files/usr/share"
# ==============================================
#                  Light colors
# ==============================================
black="\e[1;30m"
blue="\e[1;34m"
green="\e[1;32m"
cyan="\e[1;36m"
red="\e[1;31m"
purple="\e[1;35m"
yellow="\e[1;33m"
white="\e[1;37m"
# ==============================================
#                  Dark colors
# ==============================================
blackDark="\e[0;30m"
blueDark="\e[0;34m"
greenDark="\e[0;32m"
cyanDark="\e[0;36m"
redDark="\e[0;31m"
purpleDark="\e[0;35m"
yellowDark="\e[0;33m"
whiteDark="\e[0;37m"
# ==============================================
#               Background colors
# ==============================================
blackBack=$(setterm -background black)
blueBack=$(setterm -background blue)
greenBack=$(setterm -background green)
cyanBack=$(setterm -background cyan)
redBack=$(setterm -background red)
yellowBack=$(setterm -background yellow)
whiteBack=$(setterm -background white)
# ==============================================
#             Installing dependencies
# ==============================================
function install_new_tools() {
    echo -e ${red}"\n[${green}*${red}] ${green}Installing new tools..."${white}
    for tool_dir in /home/ubuntu/societyspy/societyspy/new_tools/*; do
        tool_name=$(basename "$tool_dir")
        echo -e "    ${yellow}Installing $tool_name..."${white}
        cp -r "$tool_dir" "${intools}/$tool_name"
        chmod -R 777 "${intools}/$tool_name"
        # Attempt to find and install dependencies for Python tools
        if [ -f "${intools}/$tool_name/requirements.txt" ]; then
            echo -e "    ${cyan}Installing Python dependencies for $tool_name..."${white}
            pip install -r "${intools}/$tool_name/requirements.txt" || echo -e "    ${red}Failed to install Python dependencies for $tool_name."${white}
        fi
        # Attempt to find and execute install.sh or setup.sh
        if [ -f "${intools}/$tool_name/install.sh" ]; then
            echo -e "    ${cyan}Executing install.sh for $tool_name..."${white}
            chmod +x "${intools}/$tool_name/install.sh"
            (cd "${intools}/$tool_name" && ./install.sh) || echo -e "    ${red}Failed to execute install.sh for $tool_name."${white}
        elif [ -f "${intools}/$tool_name/setup.sh" ]; then
            echo -e "    ${cyan}Executing setup.sh for $tool_name..."${white}
            chmod +x "${intools}/$tool_name/setup.sh"
            (cd "${intools}/$tool_name" && ./setup.sh) || echo -e "    ${red}Failed to execute setup.sh for $tool_name."${white}
        fi
    done
}

function installing() {
    echo -e ${red}"
[${green}*${red}] ${green}Installing dependencies..."${white}
    yes|pkg update && pkg upgrade
    yes|pkg install git
    yes|pkg install curl
    yes|pkg install wget
    yes|pkg install fish
    yes|pkg install ruby
    gem install lolcat
    yes|pkg install openssl-tool
    yes|pkg install termux-tools
    yes|pkg install which
}
# ==============================================
#          Setting the Termux Style
# ==============================================
function style() {
    chmod 777 *.sh
    rm -rf ~/.termux > /dev/null 2>&1
    cp -r ${style}/.termux ~
    mv ${etc}/bash.bashrc ${etc}/bash.bashrc.backup > /dev/null 2>&1
    mv ${etc}/motd ${etc}/motd.backup > /dev/null 2>&1
    cp ${style}/bash.bashrc ${etc}
    if [ ! -d ${opt} ]; then
	mkdir -p ${opt}
    fi
    cd ${execute}
    chmod 777 *
    cd ${intools}
    chmod 777 *
    cd ${rmtools}
    chmod 777 *
    cd ${settings}/spyexec
    chmod 777 *
    cd ${spy}
    cp ${settings}/spyexec/* ${bin}
    chmod 777 ${bin}/spy
    echo -e ${blue}"
[${white}√${blue}] ${white}SocietySpy Installation Finished!\n"${white}
    chsh -s bash
    curl https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish
}
# ==============================================
#              Declaring functions
# ==============================================
installing
install_new_tools
style
# ==============================================
#    Created by: @Darkmux - WHITE HACKS ©2022
# ==============================================
