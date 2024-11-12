<#
.SYNOPSIS
Hashes of the files in a specified folder.

.DESCRIPTION
This function goes through all the files in a given folder and calculates the hash of each file
using the default algorithm (SHA256). Using the VirusTotal API, it performs a query of the status
of each hash obtained.

.PARAMETER folderPath
The full path of the folder from which you want to obtain the file hashes.

.PARAMETER apikey
The API key obtained from the VirusTotal API when registering.

.EXAMPLE
Get-VirusTotalTest -folderPath C:\MyFiles -apikey 9ab213bk4h1213...

.EXAMPLE
$information = Get-VirusTotalTest -folderPath C:\MyFiles -apikey 9ab213bk4h1213...
$information is a dictionary type.

.NOTES
Make sure you have access permissions to the folder, and verify that the apikey has not expired to avoid errors.
#>

function Get-VirusTotalTest {
    param(
        [Parameter(Mandatory)][string]$folderPath = $(Read-Host "Ingresa la ruta de la carpeta: "),
        [Parameter(Mandatory)][string]$apiKey = $(Read-Host "Ingresa tu apikey: ")
    )

    $url = "https://www.virustotal.com/vtapi/v2/file/report"
    $algorithm = "SHA256"

    $verifyingPath = (Test-Path -Path $folderPath)

    if ($verifyingPath) {
        try {
            $listFiles = Get-ChildItem -Path $folderPath -File

            foreach ($file in $listFiles) {
                $hash = Get-FileHash -Path $file.FullName -Algorithm $algorithm 

                try {
                    $params = @{
                        apikey   = $apiKey
                        resource = $hash.Hash
                    }

                    $response = Invoke-RestMethod -Uri $url -Method Post -Body $params
                    Write-Host ("El archivo " + $file) -ForegroundColor Magenta

                    foreach ($info in $response.PSObject.Properties) {
                        Write-Host "$($info.Name): $($info.Value)"
                    }
                } catch {
                    Write-Error "Error al realizar la solicitud a la API de VirusTotal: $_" 
                }
                Start-Sleep -Seconds 3
            }
        } catch {
            Write-Error "Error al obtener el hash de los archivos: $_"
        }
    } else {
        Write-Host "No existe la carpeta especificada." -ForegroundColor Yellow
    }
}

