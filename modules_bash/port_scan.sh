#!/bin/bash 

# Variables
target="$1"          # Primer parámetro: IP o dominio
port_range="$2"      # Segundo parámetro: Rango de puertos
choice=$3

# Función para manejar errores
handle_error() {
    echo "An error occurred. Check the input parameters and try again."
    exit 1
}

# Detener el script con Ctrl+C
trap handle_error ERR

# Función para escanear puertos TCP usando nmap
scan_ports_tcp() {
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "===== TCP SCAN: $timestamp ====="
    echo "Target: $target"
    echo "Port range: $port_range"
    echo "--------------------------------"

    # Ejecutar el comando nmap y capturar el resultado
    nmap_output=$(nmap -p $port_range -T4 $target)

    if [ $? -eq 0 ]; then
        echo "$nmap_output"

        # Encontrar puertos abiertos y cerrados
        open_ports=$(echo "$nmap_output" | grep -oP '\d+/tcp\s+open' | awk '{print $1}')
        closed_ports=$(echo "$nmap_output" | grep -oP '\d+/tcp\s+closed' | awk '{print $1}')

        # Mostrar resultados en la consola
        if [ -z "$open_ports" ]; then
            echo "No open TCP ports found on $target."
        else
            echo "Open TCP ports on $target: $open_ports"
        fi

        if [ -z "$closed_ports" ]; then
            echo "No closed TCP ports found on $target."
        else
            echo "Closed TCP ports on $target: $closed_ports"
        fi
    else
        echo "Scan failed. Check the IP/Domain or port range."
    fi

    echo "================================"
    echo ""
}

# Función para escanear puertos UDP usando nmap
scan_ports_udp() {
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "===== UDP SCAN: $timestamp ====="
    echo "Target: $target"
    echo "UDP Port range: $port_range"
    echo "--------------------------------"

    nmap_output=$(nmap -sU -p $port_range -T4 $target)

    if [ $? -eq 0 ]; then
        echo "$nmap_output"

        open_ports=$(echo "$nmap_output" | grep -oP '\d+/udp\s+open' | awk '{print $1}')
        closed_ports=$(echo "$nmap_output" | grep -oP '\d+/udp\s+closed' | awk '{print $1}')

        if [ -z "$open_ports" ]; then
            echo "No open UDP ports found on $target."
        else
            echo "Open UDP ports on $target: $open_ports"
        fi

        if [ -z "$closed_ports" ]; then
            echo "No closed UDP ports found on $target."
        else
            echo "Closed UDP ports on $target: $closed_ports"
        fi
    else
        echo "UDP scan failed. Check the IP/Domain or port range."
    fi

    echo "================================"
    echo ""
}

case $choice in
    1) scan_ports_tcp ;;
    2) scan_ports_udp ;;
esac
