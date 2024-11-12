#!/usr/bin/python3

import os
import platform
import argparse
import subprocess
import csv
import hashlib
import re
from datetime import datetime
from termcolor import colored
from PowershellToPython.PyToPs import menu_powershell
from ModulesPython.honeypot_ssh import start_honeypot
from ModulesPython.modules_api import search_vulnerabilities, suspicious_ip
from ModulesPython.analyze_connections import analyze_connections
from ModulesPython.suspicious_services import suspicious_services


#
description = """Este script ejecuta varias tareas de ciberseguridad y genera un reporte en un archivo especificado."""
parser = argparse.ArgumentParser(description=description, epilog="Se debe ingresar el nombre del archivo donde se guardarán los resultados.", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--Name", dest="FileName", help="Nombre del archivo de salida para el reporte de resultados (sin extensión, el formato será añadido automáticamente)", default="Reporte")
params = parser.parse_args()
name = params.FileName
so = platform.platform()

# 
main_path = os.path.dirname(os.path.abspath(__file__))
report_directory = os.path.join(main_path, "Reportes")
os.makedirs(report_directory, exist_ok=True)

def hash_file(file_path):
        """This function calculates the SHA-256 hash of a file and prints it with the date and location."""
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
                hash = hashlib.sha256(file_data)
                hashed = hash.hexdigest()
            
            current_date = datetime.now()
            format_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
            print("Fecha:", format_date)
            print("Ruta del reporte:", file_path)
            print("Hash SHA-256:", hashed)
    
        except FileNotFoundError:
            print(f"Error: El archivo '{file_path}' no se encontró.")

        except Exception as e:
            print(f"Ocurrió un error al calcular el hash: {e}")

def menu_python(name):
    """This function has all the options that are executed in python."""
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
                start_honeypot(port)
                dir_path =  os.path.dirname(os.path.abspath(__file__))
                report_path = os.path.join(dir_path, "Reportes")
                file_path = os.path.join(report_path, f"report_ssh_honeypot.log")
                hash_file(file_path)
                
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
                    search_vulnerabilities(APIKEY,port_shodan,name)             
                else:
                    ports=input("Ingrese los puertos que quiera ver, en caso de ser mas de uno separarlos por una coma y un espacio")
                    port_shodan="port: "+str(ports)
                    search_vulnerabilities(APIKEY,port_shodan,name)       
        
            elif option == 3:
                APIKEY=input("Ingrese la API key que se usara para conectarse a la API de IPAbuseDB")
                suspicious_ip(APIKEY,name)
                    
            elif option == 4:
                try:
                    opcion_nombre=int(input("Desea editar el nombre del archivo en donde se guardará el reporte (suspicious_connections_report.txt)? 1-Si 2-No: "))
                    while (opcion_nombre <=0 or opcion_nombre>2):
                        opcion_nombre = int(input("Opicón no válida, intente nuevamente: "))
                    if opcion_nombre == 1:
                        analyze_connections(name)
                    else:
                        analyze_connections()
                except Exception: 
                    print("Ha ocurrido un error, intente nuevamente")

            elif option == 5:
                try:
                    opcion_generar_excel = int(input("Deseas conservar el excel con los procesos activos? 1-Sí 2-No: "))
                    while opcion_generar_excel<1 or opcion_generar_excel>2:
                        opcion_generar_excel = int(input("Opción no válida, vuleve a ingresarla: "))
                    suspicious_services(opcion_generar_excel)
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
    """This function has all the options that are executed in bash."""
    dir_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(dir_path, "ModulesBash")

    def menu():
        """Este menú contiene opciones específicas para tareas de Bash."""
        msg = "-"*50+"""
            MENU
        [1]. Monitoreo de red
        [2]. Escaneo de puertos
        [3]. Script de Python
    """
        print(msg)    

    while True: 
        try:
            menu()
            option = int(input("Seleccione una opción: "))
            if option == 1:
                try:
                    script_path = os.path.join(folder_path, "monitoreo_red.sh")
                    
                    # Asegura que el script tenga permisos de ejecución
                    subprocess.run(["chmod", "+x", script_path])

                    cant = input("Cantidad de veces que quiere que se realice el monitoreo: ")
                    while True:
                        try: 
                            cant = int(cant)
                            if cant <= 0:
                                print("Tiene que ser un valor positivo")
                            else:
                                break
                        except:
                            print("Tiene que ser un valor numerico")
                
                    bash_command = f"{script_path} -n {cant}"
                    result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, executable="/bin/bash")
                    result.check_returncode() 
                    data = result.stdout

                    file_name = f"{name}.csv"
                    report_path = os.path.join(dir_path, "Reportes")
                    file_path = os.path.join(report_path, f"{name}.csv")
                    lines = data.splitlines()

                    with open(file_path, 'w', newline='') as file:
                        writer = csv.writer(file)
                        for line in lines:
                            writer.writerow([line])
                    hash_file(file_name)

                except subprocess.CalledProcessError as e:
                    print(f"Error al ejecutar el comando bash: {e}")
                except Exception as e:
                    print(f"Ocurrió un error: {e}")

            elif option == 2:
                try:
                    script_path = os.path.join(folder_path, "port_scan.sh")
                    subprocess.run(["chmod", "+x", script_path])

                    while True:
                        target = input("Ingrese la IP de la que quiera escanear los puertos: ")
                        pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
                        if re.match(pattern, target):
                            break
                        else:
                            print("La IP ingresada no es válida. Intente de nuevo.")
                    
                    while True:
                        port = input("Ingrese el rango de puertos que se desea escanear (1-1000): ")
                        try:
                            port = int(port)
                            if port < 1 or port > 1000:
                                print("El puerto debe estar en el rango de 1 a 1000.")
                            else:
                                port = str(port)
                                break  
                        except:
                            print("Es un valor numerico")   
                    
                    def menu():
                        """Este menú contiene opciones específicas para tareas de Bash."""
                        msg = "-"*50+"""
                            MENU
                        [1]. Scan TCP ports
                        [2]. Scan UDP ports
                    """
                        print(msg)   
                    while True: 
                        try:
                            menu()
                            option = int(input("Seleccione una opción: "))
                            if option == 1 or option ==2 :
                                bash_command = f"{script_path} {target} {port} {option}"
                                result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, executable="/bin/bash")
                                result.check_returncode()  # Verifica si el proceso fue exitoso
                                data = result.stdout

                                report_path = os.path.join(dir_path, "Reportes")
                                file_path = os.path.join(report_path, f"{name}.txt")
                                with open(file_path, "+a") as file: 
                                   file.write(data)
                                
                                hash_file(f"{name}.txt")
                        except ValueError:
                            print(colored("Valor incorrecto, se tiene que ingresar un número entero.", 'red'))
                            continue

                except subprocess.CalledProcessError as e:
                    print(f"Error al ejecutar el comando bash: {e}")
                except Exception as e:
                    print(f"Ocurrió un error: {e}")

            elif option == 3:
                menu_python(name)
                pass

            else:
                print(colored("Opción incorrecta.", 'red'))
                continue
        except ValueError:
            print(colored("Valor incorrecto, se tiene que ingresar un número entero.", 'red'))
            continue
        except Exception as e:
            print(e)
        break 

if __name__ == "__main__":
    if "Windows" in so:
        print("El sistema operativo en el cual está ejecutándose el script es Windows.")
        print("Por lo tanto no se podrán correr los módulos de bash, pero se ejecutaran los de powershell y python.")
        print("-"*50+"\n")
        menu_powershell(name)
    elif "Linux" in so:
        print("El sistema operativo en el cual está ejecutándose el script es Linux")
        print("Por lo tanto no se podrán correr los módulos de powershell, pero se ejecutaran los de bash y python.")
        print("-"*50+"\n")
        menu_bash(name)
    else:
        print("El sistema operativo es:", so)
        print("Por lo tanto no se podrá ejecutar los módulos de bash ni powershell, pero se ejecutaran los de python.")
        print("-"*50+"\n")
        menu_python(name)
