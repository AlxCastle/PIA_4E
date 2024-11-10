#!/usr/bin/python3
import subprocess  

try: 
    bash_command = "./monitoreo_red -n 2"
    result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, executable='/bin/bash') 

    print("Salida del comando:") 
    print(result.stdout) 

    if result.stderr: 

        print("Errores:") 

        print(result.stderr) 

except Exception as e: 
    #print(f"Ocurrió un error al ejecutar la tarea: {e}") 
    pass
finally: 
    print("Ejecución completada.") 