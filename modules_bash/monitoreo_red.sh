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
#read -p "Ingrese la cantidad de veces que quiere realizar el monitoreo: " num
#network_monitoring $num
# Ask for the filename and the number of times
#read -p "Ingrese el nombre del reporte que quiere generar: " file
# Redirect the output to a file


