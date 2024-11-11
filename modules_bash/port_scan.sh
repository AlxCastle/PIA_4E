#!/bin/bash 

# Variables
target="$1"          # Primer parámetro: IP o dominio
port_range="$2"      # Segundo parámetro: Rango de puertos
name="${3:-scan_results}"  # Tercer parámetro: Nombre del archivo (por defecto: scan_results)

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

    echo "Scanning TCP ports on $target..."

    # Añadir un encabezado al archivo de resultados
    echo "===== TCP SCAN: $timestamp =====" >> "$name".txt
    echo "Target: $target" >> "$name".txt
    echo "Port range: $port_range" >> "$name".txt
    echo "--------------------------------" >> "$name".txt

    # Ejecutar el comando nmap y capturar el resultado
    nmap_output=$(nmap -p $port_range -T4 $target)

    if [ $? -eq 0 ]; then
        echo "$nmap_output" >> "$name".txt

        # Encontrar puertos abiertos y cerrados
        open_ports=$(echo "$nmap_output" | grep -oP '\d+/tcp\s+open' | awk '{print $1}')
        closed_ports=$(echo "$nmap_output" | grep -oP '\d+/tcp\s+closed' | awk '{print $1}')

        # Mostrar resultados en la consola y agregarlos al reporte
        if [ -z "$open_ports" ]; then
            echo "No open TCP ports found on $target." >> "$name".txt
        else
            echo "Open TCP ports on $target: $open_ports" >> "$name".txt
        fi

        if [ -z "$closed_ports" ]; then
            echo "No closed TCP ports found on $target." >> "$name".txt
        else
            echo "Closed TCP ports on $target: $closed_ports" >> "$name".txt
        fi
    else
        echo "Scan failed. Check the IP/Domain or port range." >> "$name".txt
        echo "Scan failed. Check the IP/Domain or port range."
    fi

    echo "================================" >> "$name".txt
    echo "" >> "$name".txt

}

# Función para escanear puertos UDP usando nmap
scan_ports_udp() {
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "Scanning UDP ports on $target..."

    echo "===== UDP SCAN: $timestamp =====" >> "$name".txt
    echo "Target: $target" >> "$name".txt
    echo "UDP Port range: $port_range" >> "$name".txt
    echo "--------------------------------" >> "$name".txt

    nmap_output=$(nmap -sU -p $port_range -T4 $target)

    if [ $? -eq 0 ]; then
        echo "$nmap_output" >> "$name".txt

        open_ports=$(echo "$nmap_output" | grep -oP '\d+/udp\s+open' | awk '{print $1}')
        closed_ports=$(echo "$nmap_output" | grep -oP '\d+/udp\s+closed' | awk '{print $1}')

        if [ -z "$open_ports" ]; then
            echo "No open UDP ports found on $target." >> "$name".txt
        else
            echo "Open UDP ports on $target: $open_ports" >> "$name".txt
        fi

        if [ -z "$closed_ports" ]; then
            echo "No closed UDP ports found on $target." >> "$name".txt
        else
            echo "Closed UDP ports on $target: $closed_ports" >> "$name".txt
        fi
    else
        echo "UDP scan failed. Check the IP/Domain or port range." >> "$name".txt
    fi

    echo "================================" >> "$name".txt
    echo "" >> "$name".txt

}


#Function that displays the menu
show_menu() {
    echo ""
    echo "======= MENU ======="
    echo "1. Scan TCP ports"
    echo "2. Scan UDP ports"
    echo "===================="
}

#Loop of the main menu
while true; do
    show_menu
    read -p "Choose an option: " choice
    case $choice in
        1)
            scan_ports_tcp
            ;;
        2)
            scan_ports_udp
            ;;
        *)
            echo "Invalid option, try again."
            ;;
    esac
done



