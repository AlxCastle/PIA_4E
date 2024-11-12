# 4o Entregable - Proyecto Final de Ciberseguridad: Integración de Módulos y Generación de Reportes 

## Descripción
Este proyecto consiste en la creación de varios scripts en Python que realizan diversas tareas de ciberseguridad: análisis de conexiones TCP, detección de servicios sospechosos, consumo de APIs (Shodan e IPAbuseDB), y la implementación de un honeypot SSH. Los scripts aceptan parámetros de entrada y cuentan con menús interactivos para diversas funcionalidades, así como el manejo de errores durante la ejecución.

## Objetivos
- Desarrollar habilidades en Python: Aplicar lo aprendido sobre Python para crear scripts que realicen tareas de ciberseguridad.
- Automatizar tareas de ciberseguridad: Facilitar la ejecución de tareas repetitivas y complejas mediante scripts automatizados.

## Requisitos
- Python 3.x
- Paquetes de Python: `paramiko`, `requests`, `termcolor`, `shodan`, `openpyxl`
- Recomendación:
    - Tener acceso a PowerShell en Windows para ejecutar varias funciones
    - Contar con el sistema operativo Linux, asi como con paquetes como  `nmap`, `ifstat`

Instala los paquetes necesarios utilizando:

```bash
pip install -r requirements.txt
```  

[main.py](http://_vscodecontentref_/2)
ModulesBash/
    [monitoreo_red.sh](http://_vscodecontentref_/3)
    [port_scan.sh](http://_vscodecontentref_/4)
ModulesPython/
    __init__.py
    __pycache__/
    [analyze_connections.py](http://_vscodecontentref_/5)
    [honeypot_ssh.py](http://_vscodecontentref_/6)
    [modules_api.py](http://_vscodecontentref_/7)
    [suspicious_services.py](http://_vscodecontentref_/8)
PowershellToPython/
    __init__.py
    __pycache__/
    Module_1/
        [Module_1.psm1](http://_vscodecontentref_/9)
    Module_2/
        [Module_2.psm1](http://_vscodecontentref_/10)
    Module_3/
        [Module_3.psm1](http://_vscodecontentref_/11)
    Module_4/
        [Module_4.psm1](http://_vscodecontentref_/12)
    [PyToPs.py](http://_vscodecontentref_/13)
[README.md](http://_vscodecontentref_/14)
[requirements.txt](http://_vscodecontentref_/15)



## Instrucciones de Uso
Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/AlxCastle/PIA_3E.git
```

Ahora cuentas con la carpeta y los scripts.

### Ejemplo de Ejecución del script principal

Ejemplo 1: Ejecutar el menu:

```bash
chmod +x main.py
```

```bash
python3 main.py
```

Seleccione una opcion del menu y siga las instrucciones que da el programa.

## Colaboradores
Este proyecto fue desarrollado en colaboración con:

- Emilio Rafael Puente Cardona
- Manuel Emilio Delgado Gómez
- Alondra Castillo Gonzalez
  
