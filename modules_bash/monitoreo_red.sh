#!/bin/bash 

# Check if the ifstat command is installed
if ! command -v ifstat &> /dev/null;
then
    echo "Error: ifstat no está instalado. Instálalo para volver a intentar."
    exit 1
fi

# Define the function to monitor the network
function network_monitoring {
    local n=$1
    for ((i=1; i<=n; i++)); do
        ifstat 5 1
        sleep 5
    done
}

# Validate the input parameter
if [ "$1" = "-n" ]; then  
    if [ -z "$2" ]; then
        echo "Requiere la cantidad de veces que quiere ver el monitoreo."
        exit 1
    elif [[ ! "$2" =~ ^-?[0-9]+$ ]]; then
        echo "Requiere un valor numerico."
        exit 1
    else
        network_monitoring "$2"
    fi
else
    echo "NOTA: Si desea ejecutar el script ingresando un parametro de entrada -n cantidad, donde cantidad representa la cantidad de veces que quiere ver el monitoreo y presione CTRL+C."
fi

# Function to display the menu
show_menu() {
    echo ""
    echo "======= MENÚ ======="
    echo "1.  Monitorear la red en vivo."
    echo "2.  Monitorear la red una cantidad predeterminada"
    echo "3.  Generar un reporte"
    echo "4.  Salir"
    echo "===================="
}


# Validate the option chosen by the user
while true; do
    show_menu
    read -p "Elige una opción: " choice
    case $choice in
        1)
            # View monitoring indefinitely
            ifstat &
            PROCESS_PID=$!
            echo "Presiona cualquier tecla y luego ENTER para detener ifstat"          
            read -r userInput
            kill $PROCESS_PID
            ;;
        2)
            # View the monitoring a defined number of times
            read -p "Ingrese la cantidad de veces que quiere ver el monitoreo: " num
            network_monitoring $num
            ;;
        3)
            # Ask for the filename and the number of times
            read -p "Ingrese el nombre del reporte que quiere generar: " file
            read -p "Ingrese la cantidad de veces que quiere ver el monitoreo: " num
            # Redirect the output to a file
            if ! network_monitoring $num > "$file"; then
                echo "Error: No se pudo generar el archivo"
                exit 1
            else
                echo "El reporte ha sido generado"
            fi
            ;;
        4)
                echo "Saliendo..."
            exit 0
            ;;
        *)
            echo "Opción no válida, intenta de nuevo."
            ;;
    esac
done
       