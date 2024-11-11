##!usr/bin/python3

from termcolor import colored
import platform
import argparse
import os
import subprocess
import csv
#from Modules.honeypot_ssh import start_honeypot
#from Modules.modules_api import search_vulnerabilities, suspicious_ip
#from Modules.analyze_connections import analyze_connections
#from Modules.suspicious_services import suspicious_services

# Descripción del script y manejo de argumentos
description = """Este script ejecuta varias tareas de ciberseguridad y genera un reporte en un archivo especificado."""
parser = argparse.ArgumentParser(description=description, epilog="Se debe ingresar el nombre del archivo donde se guardarán los resultados.", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--Name", dest="FileName", help="Nombre del archivo de salida para el reporte de resultados (sin extensión, el formato será añadido automáticamente)", default="Reporte")
params = parser.parse_args()
name = params.FileName
so = platform.platform()

def menu_python(name):
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


    while True: 
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
                #start_honeypot(port)
                data = "Reporte honeypot, revisar logs"
                with open(f"{name}.txt", "+a") as file:
                    file.write(data)
                print("Reporte realizado")
                
            elif option == 2:
                APIKEY=input("Ingrese la API key que se usara para conectarse a la API de shodan")
                if "Linux" in so:
                    def scan_ports_tcp(target="192.168.1.1", port_range="1-255"):
                        bash_command =f"./portscan {target} {port_range}"

                        # Ejecuta el comando y captura la salida
                        try:
                            result = subprocess.check_data(['bash', '-c', bash_command], text=True)
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
                continue
        except ValueError:
            print(colored("Valor incorrecto, se tiene que ingresar un numero entero.", 'red'))
            continue
        except Exception as e:
            print(e)
        break 



def menu_bash(name):
    def menu():
        """This function contains the format of the menu."""
        msg = "-"*50+"""
            MENU
        [1]. Monitoreo de red
        [2]. Escaneo de puertos
        [3]. Script de python
    """
        print(msg)    

    #script_path = os.path.dirname(os.path.abspath(__file__))
    #folder_path = os.path.join(script_path, "modules_bash")

    while True: 
        try:
            menu()
            option = int(input("Seleccione una opcion: "))
            if option==1:
                #script_path = os.path.join(folder_path, "monitoreo_red.sh")
                while True:
                    try:
                        cant = int(input("Cantidad de veces que quiere que se realice el monitoreo: "))
                        if cant < 0: 
                            print("Es un número positivo")
                        cant = str(cant)
                        break
                    except:
                        print(colored("Valor incorrecto, se tiene que ingresar un numero entero.", 'red'))
                try:
                    bash_command = f"./monitoreo_red.sh -n {cant}"
                    result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, executable="/bin/bash")
                    print(result.stderr)
                    print("Resultados:", result.stdout)
                    data = result.stdout

                    file_name = f"{name}.csv"
                    lines = data.splitlines()
                    with open(file_name, 'w', newline='') as file:
                        writer = csv.writer(file)
                        for line in lines:
                            writer.writerow([line])
                except Exception as e:
                    print(e)

            elif option == 2:
                try: 
                    script_path = os.path.join(os.getcwd(), "port_scan.sh")
                    target = input("Ingrese la IP de la que quiera escanear los puertos: ")
                    port_range = input("Ingrese el rango de puertos que se desean escanear: ")
                    bash_command = f"{script_path} {target} {port_range}"
                    result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, executable="/bin/bash")
                    print(result.stdout)
                    data = result.stdout

                    with open(f"{name}.txt", "+a") as file: 
                        file.write(data)
                except Exception as e:
                    print(e)
        

            elif option == 3:
                menu_python(FileName=name)
            else:
                print(colored("Opción incorrecta.", 'red'))
                continue
        except:
            print(colored("Valor incorrecto, se tiene que ingresar un número entero.", 'red'))
            continue
        break 


if __name__ == "__main__":
    if "Windows" in so:
        print("El sistema operativo en el cual está ejecutándose el script es Windows")
        print("Por lo tanto no se podrán correr los módulos de bash")
        menu_python(name)
    elif "Linux" in so:
        print("El sistema operativo en el cual está ejecutándose el script es Linux")
        print("Por lo tanto no se podrán correr los módulos de powershell")
        menu_bash(name)
    else:
        print("El sistema operativo es:", so)
        print("Por lo tanto no se podrá ejecutar los módulos de bash ni powershell")
        menu_python(name)



