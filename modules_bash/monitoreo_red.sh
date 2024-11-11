#!/bin/bash 

# Check if the ifstat command is installed
if ! command -v ifstat &> /dev/null;
then
    echo "Error: ifstat no está instalado. Instálalo para volver a intentar." >&2
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

#
network_monitoring "$2" 2>&1 || echo "Error: Hubo un problema al ejecutar el monitoreo." >&2
