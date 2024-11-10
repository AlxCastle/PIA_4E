<#Description: The module is responsible for showing the user the memory, disk, process, and network resources,
You will also have the option to choose between viewing the resources used at the moment, or generating a text report.
Parameters: No input parameters are needed, however, data is requested inside the module.#>
function View-Resources{
#First, the resources used are obtained in variables.
#In this command, the counter is used that calls certain processes such as network, memory, cpu, tec. The properties are converted to numbers to make it easier to read.
#The try is used to be able to execute the command if the machine is in English or Spanish   
    try{
        $UsedRAM=Get-Counter "\memoria\% de bytes confirmados en uso" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue
        $FreeRAM=100-$UsedRam
        $UsedDisk=Get-Counter "\disco físico(_Total)\% de tiempo de disco" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue
        $FreeDisk=100-$UsedDisk
        $UsedCPU=Get-Counter "\Procesador(_Total)\% de tiempo de procesador" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue
        $FreeCPU=100-$UsedCPU
        $SentRed=Get-Counter "\Interfaz de red(*)\Bytes enviados/s" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue
        $ReceivedRed=Get-Counter "\Interfaz de red(*)\Bytes recibidos/s" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue
    }catch{
        try{
            $UsedRAM=Get-Counter "\Memory\% Committed Bytes In Use" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue
            $FreeRAM=100-$UsedRam
            $UsedDisk=Get-Counter "\PhysicalDisk(_Total)\% Disk Time" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue
            $FreeDisk=100-$UsedDisk
            $UsedCPU=Get-Counter "\Processor(_Total)\% Processor Time" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue
            $FreeCPU=100-$UsedCPU
            $SentRed=Get-Counter "\\Network Interface(*)\Bytes Sent/sec" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue
            $ReceivedRed=Get-Counter "\Network Interface(*)\Bytes Received/sec" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue
        }catch{
            Write-Host "No se pudieron obtener los recursos usados"
            break
        }
    }

        Write-Host "Este es el uso de memoria libre es $FreeRAM%"
        Write-Host "Este es el uso de memoria que se esta utilizando $UsedRAM%"
        Write-Host "Este es el uso de disco libre es $FreeDisk%"
        Write-Host "Este es el uso de disco que se esta utilizando $UsedDisk%"
        Write-Host "Este es el uso de CPU(procesos) libre es $FreeCPU%"
        Write-Host "Este es el uso de CPU(procesos) que se esta utilizando $UsedCPU%" 
        Write-Host "Esta es la cantidad de bytes que se estan enviando en la red $SentRed"
        Write-Host "Esta es la cantidad de bytes que se estan recibiendo en la red $ReceivedRed"
  
    }