# 4o Entregable - Proyecto Final de Ciberseguridad: Integración de Módulos y Generación de Reportes 

## Descripción
Este proyecto consiste en la creación de varios scripts en Python que realizan diversas tareas de ciberseguridad: análisis de conexiones TCP, detección de servicios sospechosos, consumo de APIs (Shodan e IPAbuseDB), y la implementación de un honeypot SSH. Los scripts aceptan parámetros de entrada y cuentan con menús interactivos para diversas funcionalidades, así como el manejo de errores durante la ejecución. Además el script está diseñado para ejecutarse en sistemas operativos Linux, Windows y otros, aunque las tareas disponibles varían y están limitadas según el sistema operativo detectado. En Linux, el script ejecuta tareas a través de Bash y Python, mientras que en Windows, utiliza PowerShell y Python. Dependiendo del sistema operativo, algunas tareas específicas pueden no estar disponibles, pero las funcionalidades principales seguirán funcionando con las herramientas compatibles para cada plataforma.

## Objetivos
- Desarrollar habilidades en Python: Aplicar lo aprendido sobre Python para crear scripts que realicen tareas de ciberseguridad.
- Automatizar tareas de ciberseguridad: Facilitar la ejecución de tareas repetitivas y complejas mediante scripts automatizados.

## Requisitos
- Python 3.x
- Paquetes de Python: `paramiko`, `requests`, `termcolor`, `shodan`, `openpyxl`
- Recomendación:
    - Tener acceso a PowerShell en Windows para ejecutar varias funciones
    - Tener acceso a Bash en Linux, además de contar con paquetes como  `nmap`, `ifstat` ya instalados en el sistema.

Instala los paquetes necesarios utilizando:

```bash
pip install -r requirements.txt
```  

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
  
