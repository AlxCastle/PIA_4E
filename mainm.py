#!/usr/bin/python3

from termcolor import colored
import platform
import argparse
import os
import subprocess
import csv
import hashlib
import re
from datetime import datetime

# Descripción del script y manejo de argumentos
description = """Este script ejecuta varias tareas de ciberseguridad y genera un reporte en un archivo especificado."""
parser = argparse.ArgumentParser(description=description, epilog="Se debe ingresar el nombre del archivo donde se guardarán los resultados.", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--Name", dest="FileName", help="Nombre del archivo de salida para el reporte de resultados (sin extensión, el formato será añadido automáticamente)", default="Reporte")
params = parser.parse_args()
name = params.FileName
so = platform.platform()

def hash_file(file_path):
    """Calcula el hash SHA-256 de un archivo y lo imprime junto con la fecha y ubicación del archivo."""
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


def menu_bash(name):
    def menu():
        """Este menú contiene opciones específicas para tareas de Bash."""
        msg = "-"*50+"""
            MENU
        [1]. Monitoreo de red
        [2]. Escaneo de puertos
        [3]. Script de Python
    """
        print(msg)    

    dir_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(dir_path, "modules_bash")

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
                            if cant <1:
                                print("Tiene que ser un valor positivo")
                            else:
                                break
                        except:
                            print("Tiene que ser un valor numerico")
                
                    bash_command = f"{script_path} -n {cant}"
                    result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, executable="/bin/bash")
                    result.check_returncode()  # Verifica si el proceso fue exitoso
                    print(result.stderr)
                    data = result.stdout

                    file_name = f"{name}.csv"
                    lines = data.splitlines()
                    with open(file_name, 'w', newline='') as file:
                        writer = csv.writer(file)
                        for line in lines:
                            writer.writerow([line])
                    
                    # Llamar a hash_file para imprimir el hash
                    hash_file(file_name)

                except subprocess.CalledProcessError as e:
                    print(f"Error al ejecutar el comando bash: {e}")
                except Exception as e:
                    print(f"Ocurrió un error: {e}")

            elif option == 2:
                try:
                    script_path = os.path.join(folder_path, "port_scan.sh")
                    
                    # Asegura que el script tenga permisos de ejecución
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

                    bash_command = f"{script_path} {target} {port} {folder_path}"
                    result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, executable="/bin/bash")
                    result.check_returncode()  # Verifica si el proceso fue exitoso
                    print("Concluido")
                    print(result.stdout)
                    #data = result.stdout

                    #with open(f"{name}.txt", "+a") as file: 
                    #    file.write(data)
                    
                    # Llamar a hash_file para imprimir el hash
                    #hash_file(f"{name}.txt")

                except subprocess.CalledProcessError as e:
                    print(f"Error al ejecutar el comando bash: {e}")
                except Exception as e:
                    print(f"Ocurrió un error: {e}")

            elif option == 3:
                # Llama al menú de Python si se selecciona esta opción
                #menu_python(name)
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
        print("El sistema operativo en el cual está ejecutándose el script es Windows")
        print("Por lo tanto no se podrán correr los módulos de bash")
        # Aquí iría el llamado al menú de PowerShell
    elif "Linux" in so:
        print("El sistema operativo en el cual está ejecutándose el script es Linux")
        print("Por lo tanto no se podrán correr los módulos de PowerShell")
        menu_bash(name)
    else:
        print("El sistema operativo es:", so)
        print("Por lo tanto no se podrá ejecutar los módulos de bash ni PowerShell")
        # Aquí iría el llamado al menú de Python si se desea
