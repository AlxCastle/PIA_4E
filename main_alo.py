#!/usr/bin/python3

from termcolor import colored
import platform
import argparse
import os
import subprocess
import csv
import pandas as pd

# Descripción del script y manejo de argumentos
description = """Este script ejecuta varias tareas de ciberseguridad y genera un reporte en un archivo especificado."""
parser = argparse.ArgumentParser(description=description, epilog="Se debe ingresar el nombre del archivo donde se guardarán los resultados.", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--Name", dest="FileName", help="Nombre del archivo de salida para el reporte de resultados (sin extensión, el formato será añadido automáticamente)", default="Reporte")
params = parser.parse_args()
name = params.FileName
so = platform.platform()

def menu_python(FileName):
    def menu():
        """This function contains the format of the menu."""
        msg = "-"*50 + """
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

            # Validate the port.
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

        elif option == 2:
            APIKEY = input("Ingrese la API key que se usara para conectarse a la API de shodan")
            if "Linux" in so:
                def scan_ports_tcp(target="192.168.1.1", port_range="1-255"):
                    bash_command = f"./portscan {target} {port_range}"

                    # Ejecuta el comando y captura la salida
                    try:
                        result = subprocess.check_output(['bash', '-c', bash_command], text=True)
                        open_ports = result.strip()
                        return open_ports  # Devuelve los puertos abiertos encontrados
                    except subprocess.CalledProcessError as e:
                        print(f"Error during scan: {e}")
                        return None
                Ports = scan_ports_tcp()
                port_shodan = "port: " + str(Ports)
            else:
                ports = input("Ingrese los puertos que quiera ver, en caso de ser mas de uno separarlos por una coma y un espacio")
                port_shodan = "port: " + str(ports)

        elif option == 3:
            APIKEY = input("Ingrese la API key que se usara para conectarse a la API de IPAbuseDB")

        elif option == 4:
            try:
                opcion_nombre = int(input("Desea editar el nombre del archivo en donde se guardará el reporte (suspicious_connections_report.txt)? 1-Si 2-No: "))
                while (opcion_nombre <= 0 or opcion_nombre > 2):
                    opcion_nombre = int(input("Opción no válida, intente nuevamente: "))
            except Exception:
                print("Ha ocurrido un error, intente nuevamente")

        elif option == 5:
            try:
                opcion_generar_excel = int(input("Deseas conservar el excel con los procesos activos? 1-Sí 2-No: "))
                while opcion_generar_excel < 1 or opcion_generar_excel > 2:
                    opcion_generar_excel = int(input("Opción no válida, vuelve a ingresarla: "))
            except Exception:
                print("Ha ocurrido un error, inténtalo de nuevo")

        else:
            print(colored("Opcion incorrecta.", 'red'))
    except ValueError:
        print(colored("Valor incorrecto, se tiene que ingresar un numero entero.", 'red'))


def menu_bash():
    def menu():
        """This function contains the format of the menu."""
        msg = "-"*50 + """
            MENU
        [1]. Monitoreo de red
        [2]. Escaneo de puertos
        [3]. En caso de querer ejecutar un script de python
        """
        print(msg)

    try:
        menu()
        option = int(input("Seleccione una opcion: "))
        if option == 1:
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

        elif option == 2:
            script_path = os.path.join(os.getcwd(), "port_scan.sh")
            target = input("Ingrese la IP de la que quiera escanear los puertos: ")
            port_range = input("Ingrese el rango de puertos que se desean escanear: ")
            bash_command = f"{script_path} {target} {port_range}"
            result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, executable="/bin/bash")
            print(result.stdout)

        elif option == 3:
            menu_python(FileName=file_name)
        else:
            print(colored("Opción incorrecta.", 'red'))
    except:
        print(colored("Valor incorrecto, se tiene que ingresar un número entero.", 'red'))

if __name__ == "__main__":
    if "Windows" in so:
        print("El sistema operativo en el cual está ejecutándose el script es Windows")
        print("Por lo tanto no se podrán correr los módulos de bash")
        menu_python(file_name)
    elif "Linux" in so:
        print("El sistema operativo en el cual está ejecutándose el script es Linux")
        print("Por lo tanto no se podrán correr los módulos de powershell")
        menu_bash()
    else:
        print("El sistema operativo es:", so)
        print("Por lo tanto no se podrá ejecutar los módulos de bash ni powershell")
        menu_python()

        
    else:
        print("El sistema operativo es:",so)
        print("Por lo tanto no se podra ejecutar los modulos de bash ni powershell")
        menu_python()
