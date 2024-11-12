# FolderPermisisons

# .SYNOPSIS
# Retrieves the permissions of a specified folder.
#
# .DESCRIPTION
# This function takes a folder path and returns the Access Control List (ACL) and the assigned permissions of the folder.
#
# .PARAMETER FolderPath
# The path of the folder whose permissions you want to retrieve.
#
# .EXAMPLE
# Get-FolderPermissions -FolderPath "C:\MyFolder"
#
# This command returns the permissions of the folder 'C:\MyFolder'.
#
# .NOTES
# You need to have the appropriate permissions to access the folders you are inspecting.
function Get-FolderPermissions {# Function to obtain the permissions of a folder
    
    param (
        [string]$FolderPath  #Path of the folder
    )

    # Checks if the folder exists at the specified path
    if (Test-Path $FolderPath) {
        # If the folder exists, retrieve the Access Control List (ACL) associated with the folder (the permissions of the folder), and return them
        $acl = Get-Acl -Path $FolderPath
        return $acl.Access
    } else {
       # If the folder does not exist, display an error message to the user and return null
        Write-Host "La carpeta '$FolderPath' no existe."
        return $null
    }
}



# .SYNOPSIS
# Displays the permissions of a specified folder.
#
# .DESCRIPTION
# This function takes a folder path and displays the associated permissions, including the user or group,
# the assigned rights, the type of permission (allowed or denied), and whether the permissions are inherited.
#
# .PARAMETER FolderPath
# The path of the folder whose permissions you want to display.
#
# .EXAMPLE
# Show-Permissions -FolderPath "C:\MyFolder"
#
# This command displays the permissions of the folder 'C:\MyFolder'.
#
# .NOTES
# To view the folder's permissions, you must have the necessary access rights to do so.
function Show-Permissions { # Function to view the permissions of a folder
    param (
        [string]$FolderPath  # Ruta de la carpeta para la cual se desean mostrar los permisos
    )
    # Path of the folder whose permissions will be showed
    $permissions = Get-FolderPermissions -FolderPath $FolderPath
    
    # Verifica si se obtuvieron permisos válidos
    if ($permissions) {
        Write-Host "Permisos para '$FolderPath':"
        Write-Host "----------------------------------------"
        
        # Checks if valid permissions were obtained
        $permissions | ForEach-Object {
            Write-Host ""  

            # Shows the information of each property
            Write-Host "Usuario/Grupo: $($_.IdentityReference)"          # User or group that the permisisons are applied to
            Write-Host "Derechos: $($_.FileSystemRights)"               # Access rights (such as ReadAndExecute, WriteData, etc.)
            Write-Host "Tipo: $($_.AccessControlType)"                  # Type of permission (Allow or Deny)
            Write-Host "Heredado: $($_.IsInherited) `n"                 # Indicates whether the permission is inherited or not
            
            # Prints the rights according to the assigned ones

            if ($_.FileSystemRights -eq "FullControl") {
                Write-Host "  Detalle: Control total sobre la carpeta, incluyendo lectura, escritura, y modificación de permisos."
            } elseif ($_.FileSystemRights -eq "ReadAndExecute") {
                Write-Host "  Detalle: Permiso para leer y ejecutar archivos en la carpeta."
            } elseif ($_.FileSystemRights -eq "Read") {
                Write-Host "  Detalle: Permiso para leer archivos en la carpeta, pero sin posibilidad de ejecutar archivos."
            } elseif ($_.FileSystemRights -eq "Write") {
                Write-Host "  Detalle: Permiso para escribir en la carpeta, incluyendo la creación de archivos y modificación de archivos existentes."
            } elseif ($_.FileSystemRights -eq "Modify") {
                Write-Host "  Detalle: Permiso para leer, escribir y modificar archivos en la carpeta."
            } else {
                Write-Host "  Detalle: Otros derechos de acceso. ($($_.FileSystemRights))"
            }

            Write-Host "----------------------------------------"
        }
    } else {
        # In case the permissions could not be obtained

        Write-Host "No se pudieron obtener los permisos para la carpeta '$FolderPath'."
    }
}



# .SYNOPSIS
# Compares the permissions of two specified folders.
# 
# .DESCRIPTION
# This function takes two folder paths and compares the permissions of both, showing the differences
# in terms of rights, permission types, and whether the permissions are inherited or not.
#
# .PARAMETER Folder1
# Path of the first folder whose permissions will be compared.
#
# .PARAMETER Folder2
# Path of the second folder whose permissions will be compared.
#
# .EXAMPLE
# Compare-Permissions -Folder1 "C:\Folder1" -Folder2 "C:\Folder2"
#
# This command compares the permissions between 'C:\Folder1' and 'C:\Folder2'.
#
# .NOTES
# You need the appropriate permissions to access and compare both folders.
function Compare-Permissions { # Function to compare permissions between two folders
    param (
        #Paths of the folders
        [string]$Folder1,  
        [string]$Folder2   
    )
    
    # Retrieves the permissions of the first folder using the Get-FolderPermissions function
    $permissions1 = Get-FolderPermissions -FolderPath $Folder1
    
    #Retrieves the permissions of the second folder using the Get-FolderPermissions function
    $permissions2 = Get-FolderPermissions -FolderPath $Folder2

    # Checks if both sets of permissions were obtained successfully
    if ($permissions1 -and $permissions2) {
        Write-Host "Comparando permisos entre '$Folder1' y '$Folder2'..."
        Write-Host "------------------------------------------------------"
        
        # Compares the permission entries of both folders using Compare-Object with the properties IdentityReference, FileSystemRights, AccessControlType, and IsInherited
        $diff = Compare-Object $permissions1 $permissions2 -Property IdentityReference, FileSystemRights, AccessControlType, IsInherited
        
        # If there are differences, display them
        if ($diff) {
            Write-Host "Diferencias encontradas:"
            Write-Host "------------------------------------------------------"
            
            # Iterate through each difference found
            $diff | ForEach-Object {
                # Determina si la diferencia es solo en la primera o la segunda carpeta
                if ($_.SideIndicator -eq "<=") {
                    Write-Host "Solo en '$Folder1':"
                } elseif ($_.SideIndicator -eq "=>") {
                    Write-Host "Solo en '$Folder2':"
                }
                
                # Display the differences
                Write-Host "  Usuario/Grupo: $($_.IdentityReference)"  # User or group that the permisisons are applied to
                Write-Host "  Derechos: $($_.FileSystemRights)"       # Access rights (such as ReadAndExecute, WriteData, etc.)
                Write-Host "  Tipo de permiso: $($_.AccessControlType)" # Type of permission (Allow or Deny)
                Write-Host "  Heredado: $($_.IsInherited)"           # Indicates whether the permission is inherited or not
                Write-Host "------------------------------------------------------"
            }
        } else {
            # If there are no differences, print that the permissions are identical
            Write-Host "Los permisos son idénticos entre '$Folder1' y '$Folder2'."
        }
    } else {
        # If the permissions could not be retrieved, display an error message
        Write-Host "No se pudieron obtener los permisos para una o ambas carpetas."
    }
}