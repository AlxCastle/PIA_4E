import os
import subprocess
import hashlib
from datetime import datetime

#Gets the current path of the Python script
module_path= os.path.dirname(os.path.abspath(__file__))


#This function import the powershell modules
def import_powershell_modules(module_path):
    try:
        modules=[
         "Module_1\\Module_1.psm1",
         "Module_2\\Module_2.psm1",
            "Module_3\\Module_3.psm1",
            "Module_4\\Module_4.psm1"
        ]

        for module in modules:
            module_full_path= os.path.join(module_path, module)
            command= f'Import-Module "{module_full_path}"'
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", command], capture_output=True, text=True)
    except: 
        print("No se han podido importar los módulos correctamente")


#Function that execute commands in powershell, then save the output in a txt file which is the report of the selected option and also prints the information required in the console
def execute_powershell(command, output_file, opc):
    fecha= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result= subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", command], capture_output=True, text=True)
    if result.returncode == 0:
        with open(output_file, "w") as f:
            f.write(f"------------{fecha}------------\n")
            f.write(f"{result.stdout}\n")  # Guardamos la salida del comando en un archivo
        tareas={"1":"1. Revisión de hashes de archivos y consulta a la API de VirusTotal",
                "2":"2. Listado de archivos ocultos en una carpeta",
                "3":"3. Revisión de uso de recursos del sistema",
                "4":"4. Ver permisos de las carpetas (Tarea adicional de ciberseguridad)"}
        print(f"------------{fecha}------------")
        print(f"Tarea {tareas[opc]} ejecutada con éxito")
        print(f"Archivo guardado en {output_file}")
        print(f"Hash del archivo: {get_file_hash(output_file)}")
        print(f"Ubicación del archivo: {output_file} \n")
    else:
        print("Error:", result.stderr)


#Function that gets the hash of the report generated
def get_file_hash(file_path):
    sha256_hash= hashlib.sha256()
    with open(file_path, "rb") as f:
        # Leer el archivo por bloques
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def menu_python(FileName):
    def menu():
        """This function contains the format of the menu."""
        msg = "-"*50+"""
            MENU
        [1]. Iniciar SSH Honeypot
        [2]. Consultar API Shodan
        [3]. Consultar API IPAbuseD
        [4]. Analizar conexiones
        [5]. Servicios sospechosos
    """
        print(msg)

    try:
        menu()
        option = int(input("Seleccione una opcion: "))
        
        if option == 1: 
            port = input("Puerto para vincular el servidor SSH (default 2222): ")
            
            #Validate the port.
            while True:
                try: 
                    if port == "":
                        port = 2222
                        break 
                    else: 
                        port = int(port)
                        while port < 1024 or port > 65535:
                            port = int(input("Ingrese el puerto en un rango de 1024-65535: "))
                        break 
                except ValueError: 
                    port = input("Es un dato numérico, si no desea ingresar un puerto presione enter: ")
#            start_honeypot(port)
            
        elif option == 2:
            APIKEY=input("Ingrese la API key que se usara para conectarse a la API de shodan")
            if "Linux" in so:
                def scan_ports_tcp(target="192.168.1.1", port_range="1-255"):
                    bash_command =f"./portscan {target} {port_range}"

                    # Ejecuta el comando y captura la salida
                    try:
                        result = subprocess.check_output(['bash', '-c', bash_command], text=True)
                        open_ports = result.strip()
                        return open_ports  # Devuelve los puertos abiertos encontrados
                    except subprocess.CalledProcessError as e:
                        print(f"Error during scan: {e}")
                        return None   
                Ports=scan_ports_tcp() 
                port_shodan="port: "+str(ports)
    #           search_vulnerabilities(APIKEY,port_shodan,FileName)             
            else:
                ports=input("Ingrese los puertos que quiera ver, en caso de ser mas de uno separarlos por una coma y un espacio")
                port_shodan="port: "+str(ports)
    #           search_vulnerabilities(APIKEY,port_shodan,FileName)       
     
        elif option == 3:
            APIKEY=input("Ingrese la API key que se usara para conectarse a la API de IPAbuseDB")
#           suspicious_ip(APIKEY,FileName)
                
        elif option == 4:
            try:
                opcion_nombre=int(input("Desea editar el nombre del archivo en donde se guardará el reporte (suspicious_connections_report.txt)? 1-Si 2-No: "))
                while (opcion_nombre <=0 or opcion_nombre>2):
                    opcion_nombre = int(input("Opicón no válida, intente nuevamente: "))
                if opcion_nombre == 1:
                    print()###Borrar
#                   analyze_connections(FileName)
                else:
                    print()###Borrar
#                   analyze_connections()
            except Exception: 
                print("Ha ocurrido un error, intente nuevamente")

        elif option == 5:
            try:
                opcion_generar_excel = int(input("Deseas conservar el excel con los procesos activos? 1-Sí 2-No: "))
                while opcion_generar_excel<1 or opcion_generar_excel>2:
                    opcion_generar_excel = int(input("Opción no válida, vuleve a ingresarla: "))
#               suspicious_services(opcion_generar_excel)
            except Exception:
                print("Ha ocurrido un error, intentalo de nuevo")
                
        else:   
            print(colored("Opcion incorrecta.", 'red'))
    except ValueError:
        print(colored("Valor incorrecto, se tiene que ingresar un numero entero.", 'red'))

#Display the menu
def show_menu():
    print("*** MENU ***")
    print("1. Revisión de hashes de archivos y consulta a la API de VirusTotal")
    print("2. Listado de archivos ocultos en una carpeta")
    print("3. Revisión de uso de recursos del sistema")
    print("4. Ver permisos de las carpetas (Tarea adicional de ciberseguridad)")
    print("5. Ver las actividades de python")

#Main function
def menu_powershell(name):
    import_powershell_modules(module_path)
    opcion= "0"
    while opcion != range(1,6):
        show_menu()
        opcion= input("Seleccione una opción: ")

        if opcion == "1":
            print("Revisión de hashes de archivos y consulta a la API de VirusTotal.")
            output_file= os.path.join(module_path, "Reportes/VirusTotalOutput.txt")
            execute_powershell("Get-VirusTotalTest", output_file, opcion)

        elif opcion == "2":
            path= input("Ingrese la ruta que desee ver los archivos ocultos: ")
            opcion_archivos= int(input("Presione [1]-Para ver solo los archivos ocultos [2]-Para ver todos los archivos incluyendo los ocultos: "))
            while opcion_archivos != 1 and opcion_archivos != 2:
                opcion_archivos= int(input("Opción inválida, intenta nuevamente: "))
            output_file= os.path.join(module_path, "Reportes\HiddenFilesOutput.txt")
            execute_powershell(f'Show-HiddenFiles -path "{path}" -op {opcion_archivos}', output_file, opcion)

        elif opcion == "3":
            print("Revisión de uso de recursos del sistema.")
            output_file= os.path.join(module_path, "Reportes\ResourcesOutput.txt")
            execute_powershell("View-Resources", output_file, opcion)

        elif opcion == "4":
            opcion2= input("Elige la opción a realizar: 1-Ver permisos de una carpeta en específico 2-Comparar permisos entre dos carpetas: ")

            if opcion2 == "1":
                path= input("Ingrese la ruta de la carpeta que desea ver sus permisos: ")
                output_file= os.path.join(module_path, "Reportes\PermissionsOutput.txt")
                execute_powershell(f'Show-Permissions -FolderPath "{path}"', output_file, opcion)

            elif opcion2 == "2":
                path1= input("Ingrese la ruta de la primera carpeta: ")
                path2= input("Ingrese la ruta de la segunda carpeta: ")
                output_file= os.path.join(module_path, "Reportes\ComparePermissionsOutput.txt")
                execute_powershell(f'Compare-Permissions -Folder1 "{path1}" -Folder2 "{path2}"', output_file, opcion)
            else:
                print("Opción no válida, vuelve a intentarlo.")

        elif opcion == "5":
            menu_python(name)
            break

        else:
            print("Opción inválida, seleccione una opción válida.")
