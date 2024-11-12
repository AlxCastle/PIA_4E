<#
Description:The function is used to see the hidden files in a path or to see all the files including the hidden ones, with the relevant validations
Parameters: The only parameter requested is a route, it is mandatory since if the parameter does not exist the function is of no use, it has a try to verify that the route exists
#>
function Show-HiddenFiles{
    param([Parameter(Mandatory)][string]$path,
          [Parameter(Mandatory)][int]$op )
#It starts with a try to be able to end the function in case the route does not exist
<#The get-childitem works to get the files that exist in the desired path, then forces all the files to be shown. 
hidden files and they are the ones that it collects in the case of the first variable, in the second variable it only obtains all the files including the hidden ones#>
    try{
        $hidden_files=Get-ChildItem -Path $path -Force -ErrorAction Stop | Where-Object { $_.Attributes -band [System.IO.FileAttributes]::Hidden
        $all_files=Get-ChildItem -Path $path -Force }
    }
    catch{
        Write-Host "La ruta de acceso no es válida."
        break
    }
#Here the conditional is used to choose between the options that the user chose to show the folders
    if($op -eq 1){
        if($hidden_files.Count -gt 0){
            foreach($file in $hidden_files){
                Write-host $file.FullName
            }
        } else {
            Write-Host "No se encontraron archivos ocultos."
        }
    }else{
        if($all_files.Count -gt 0){
            foreach($file in $all_files){
                Write-Host $file.FullName
            }
        }else{
            Write-Host "No se encontraron archivos en la ruta"
        }
    }
}
