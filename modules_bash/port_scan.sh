#!/bin/bash 

# Variables
target="$1"          # Primer parámetro: IP o dominio
port_range="$2"      # Segundo parámetro: Rango de puertos
name="${3:-scan_results}"  # Tercer parámetro: Nombre del archivo (por defecto: scan_results)
auto_generate_report=false     # Parámetro de reporte en HTML
scan_udp=false                 # Activar escaneo UDP

# Función para manejar errores
handle_error() {
    echo "An error occurred. Check the input parameters and try again."
    exit 1
}

# Detener el script con Ctrl+C
trap handle_error ERR

# Función para escanear puertos TCP usando nmap
scan_ports_tcp() {
    if [ -z "$target" ] || [ -z "$port_range" ]; then
        read -p "Enter the IP or domain to scan: " target
        read -p "Enter the port range to scan (example: 1-1000): " port_range
    fi

    # Obtener la fecha y hora actuales
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
            echo "No open TCP ports found on $target."
        else
            echo "Open TCP ports on $target: $open_ports" >> "$name".txt
            echo "Open TCP ports on $target: $open_ports"
        fi

        if [ -z "$closed_ports" ]; then
            echo "No closed TCP ports found on $target." >> "$name".txt
            echo "No closed TCP ports found on $target."
        else
            echo "Closed TCP ports on $target: $closed_ports" >> "$name".txt
            echo "Closed TCP ports on $target: $closed_ports"
        fi
    else
        echo "Scan failed. Check the IP/Domain or port range." >> "$name".txt
        echo "Scan failed. Check the IP/Domain or port range."
    fi

    echo "================================" >> "$name".txt
    echo "" >> "$name".txt

    if [ "$auto_generate_report" = true ]; then
        generate_report
    fi

    target=""
    port_range=""
}

# Función para escanear puertos UDP usando nmap
scan_ports_udp() {
    if [ -z "$target" ] || [ -z "$port_range" ]; then
        read -p "Enter the IP or domain to scan: " target
        read -p "Enter the UDP port range to scan (example: 1-1000): " port_range
    fi

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
            echo "No open UDP ports found on $target."
        else
            echo "Open UDP ports on $target: $open_ports" >> "$name".txt
            echo "Open UDP ports on $target: $open_ports"
        fi

        if [ -z "$closed_ports" ]; then
            echo "No closed UDP ports found on $target." >> "$name".txt
            echo "No closed UDP ports found on $target."
        else
            echo "Closed UDP ports on $target: $closed_ports" >> "$name".txt
            echo "Closed UDP ports on $target: $closed_ports"
        fi
    else
        echo "UDP scan failed. Check the IP/Domain or port range." >> "$name".txt
        echo "UDP scan failed. Check the IP/Domain or port range."
    fi

    echo "================================" >> "$name".txt
    echo "" >> "$name".txt

    if [ "$auto_generate_report" = true ]; then
        generate_report
    fi

    target=""
    port_range=""
}

# Función para analizar resultados
analyze_results() {
    if [ ! -f "$name".txt ]; then
        echo "No scan results available. Perform a scan first."
        return
    fi
    echo "Analyzing results..."
    open_ports=$(grep -oP 'open' "$name".txt | wc -l)
    closed_ports=$(grep -oP 'closed' "$name".txt | wc -l)
    echo "Open ports: $open_ports"
    echo "Closed ports: $closed_ports"
}

# Función para limpiar archivos de resultados anteriores
clear_results() {
    rm -f "$name".txt "$name".html
    echo "Previous results cleared."
}

#Function that displays the menu
show_menu() {
    echo ""
    echo "======= MENU ======="
    echo "1. Scan TCP ports"
    echo "2. Scan UDP ports"
    echo "4. Analyze results"
    echo "5. Clear results"
    echo "===================="
}

#Process the parameters
while getopts ":t:p:ru" opt; do
    case $opt in
        t) target="$OPTARG" ;; #IP or domain
        p) port_range="$OPTARG" ;; #Port range
        r) auto_generate_report=true ;; #Automatically generate the report
        u) scan_udp=true ;; #Enable UDP scan
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

#Check if input parameters were provided
if [ -n "$target" ] && [ -n "$port_range" ]; then
    if [ "$scan_udp" = true ]; then
        scan_ports_udp
    else
        scan_ports_tcp
    fi
    exit 0
fi

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
        3)
            generate_report
            ;;
        4)
            analyze_results
            ;;
        5)
            clear_results
            ;;
        *)
            echo "Invalid option, try again."
            ;;
    esac
done
