#!/bin/bash
#
# SocietySpy: Open Source
# License: General Public License
# System: GNU/linux
# Date: 22-04-2022
#
# Reestructurado por: moisesgood4-beep
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
#             Auto-Cleanup Function
# ==============================================
function auto_cleanup() {
    echo -e ${red}"[${green}*${red}] ${green}Buscando instalaciones previas..."${white}
    if [ -d "${spy}" ]; then
        echo -e ${yellow}"[${red}!${yellow}] ${red}Se detectó una versión anterior de SocietySpy. Eliminando..."${white}
        rm -rf "${spy}"
        rm -f "${bin}/spy"
        echo -e ${green}"[${white}√${green}] Limpieza completada."${white}
    else
        echo -e ${green}"[${white}√${green}] No se detectaron instalaciones previas. Procediendo..."${white}
    fi
}

# ==============================================
#             Installing dependencies
# ==============================================
function install_all_tools_and_deps() {
    echo -e ${red}"\n[${green}*${red}] ${green}Instalando TODAS las herramientas y dependencias nativas..."${white}
    
    # Crear carpeta de herramientas si no existe
    if [ ! -d "${intools}" ]; then
        mkdir -p "${intools}"
    fi

    # Mover herramientas nativas a la carpeta de instalación
    if [ -d "new_tools" ]; then
        cp -r new_tools/* "${intools}/"
        chmod -R 777 "${intools}"
    fi

    # Bucle para instalar dependencias de cada herramienta
    for tool_dir in ${intools}/*; do
        if [ -d "$tool_dir" ]; then
            tool_name=$(basename "$tool_dir")
            echo -e "    ${yellow}Configurando $tool_name..."${white}
            
            # Python dependencies
            if [ -f "$tool_dir/requirements.txt" ]; then
                echo -e "    ${cyan}Instalando dependencias de Python para $tool_name..."${white}
                pip install -r "$tool_dir/requirements.txt" --quiet
            fi
            
            # Node.js dependencies
            if [ -f "$tool_dir/package.json" ]; then
                echo -e "    ${cyan}Instalando dependencias de Node.js para $tool_name..."${white}
                (cd "$tool_dir" && npm install --quiet)
            fi

            # Ejecutar scripts de instalación si existen
            if [ -f "$tool_dir/install.sh" ]; then
                chmod +x "$tool_dir/install.sh"
                (cd "$tool_dir" && ./install.sh --quiet)
            elif [ -f "$tool_dir/setup.sh" ]; then
                chmod +x "$tool_dir/setup.sh"
                (cd "$tool_dir" && ./setup.sh --quiet)
            fi
        fi
    done
}

function installing() {
    echo -e ${red}"
[${green}*${red}] ${green}Instalando dependencias base del sistema..."${white}
    yes|pkg update && pkg upgrade
    yes|pkg install git curl wget fish ruby php python nodejs-lts which openssl-tool termux-tools
    gem install lolcat
    pip install --upgrade pip
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
    # Asegurarnos de que el directorio de destino exista antes de copiar
    mkdir -p "${spy}"
    cp -r * "${spy}/"
    cp ${settings}/spyexec/* ${bin}
    chmod 777 ${bin}/spy
    echo -e ${blue}"
[${white}√${blue}] ${white}¡Instalación de SocietySpy Finalizada!\n"${white}
    echo -e ${yellow}"Usa el comando 'spy' seguido del nombre de la herramienta para ejecutarla."${white}
    echo -e ${yellow}"Ejemplo: spy zphishing-master"${white}
    chsh -s bash
}

# ==============================================
#              Declaring functions
# ==============================================
auto_cleanup
installing
install_all_tools_and_deps
style
