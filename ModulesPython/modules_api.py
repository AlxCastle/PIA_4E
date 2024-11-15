import shodan
import logging
import requests
import json

#Function to search for vulnerabilities in different ports for different IPS

def search_vulnerabilities(APIKEY,Port_shodan,Name):
    logging.basicConfig(filename='module_shodan.log', level=logging.INFO)
    try:
        logging.info("Se intenta entrar en la api con la apikey: %s" % APIKEY)
        shodan_api=shodan.Shodan(APIKEY)

    except Exception as e:
        logging.error("Se crea un error debido a que la API KEY es invalida o no tiene los permisos requeridos")
        print("Hubo un error con la apikey\n", e)
        exit()

    else:

        try:
            logging.info("Se intenta buscar IPs con los puertos antes determinados: %s" % Port_shodan)
            result=shodan_api.search(Port_shodan)

        except Exception as e:
            logging.error("Error al poner los puertos")
            print("Hubo un error con la búsqueda\n", e)
            exit()

        else:
            logging.info("Se pide el nombre del archivo para generarlo")
            file_name=Name

            try:
                logging.info("Se intenta crear el archivo")
                with open(file_name,"w") as file:
                    for match in result["matches"]:

                        #the same thing is searched but instead of printing everything \
                        # it will be saved in a text file

                        if match["ip_str"] is not None:
                            file.write("IP: "+str(match['ip_str']))
                            file.write("Puerto: "+str(match['port']))

                            if 'vulns' in match:
                                file.write("Vulnerabilidades encontradas:")
                                for vuln in match["vulns"]:
                                    file.write("Este es el codigo de vulnerabilidad: "\
                                            +str(vuln)+"esta es el resumen del codigo:"+\
                                                str(match["vulns"][vuln]["summary"]))
                                        
                            else:
                                file.write("No se encontraron vulnerabilidades.")

                            if match["location"]["city"] is not None:
                                file.write("Ciudad de la IP: "+str(match["location"]["city"]))
                            file.write("-" * 50)

            except Exception as e:
                logging.error("Se creo un error debido a que el nombre no es valido")
                print("Hubo un problema al hacer el archivo\n", e)
    finally:
        print("La funcion ha terminado de ejecutarse")

#Function to search suspicious IPs and show the reports that are made

def suspicious_ip(APIKEY,Name):
    logging.basicConfig(filename='module_IPAbuseDB.log', level=logging.INFO)

    logging.info("Primero se obtiene en variables la url y todo lo que se ocupa para conectarse a la API")
    url_blacklist = 'https://api.abuseipdb.com/api/v2/blacklist'
    
    #The url variables and parameters are being saved to connect with the Blacklist function api

    querystring_blacklist={
        'confidenceMinimum':'90'
    }

    #The headers are saved with the APIKEY

    headers_blacklist={
        'Accept': 'application/json',
        'Key': APIKEY
    }

    #The url and header variables of the API check function are saved

    url_check='https://api.abuseipdb.com/api/v2/check'

    headers_check={
        'Accept': 'application/json',
        'Key': APIKEY
    }

    try:
        logging.info("Se conecta con la API en cuanto a la Blacklist")
        r_blacklist=requests.get(url_blacklist, headers=headers_blacklist, params=querystring_blacklist)
        r_json_blacklist=r_blacklist.json()
        len_blacklist=r_json_blacklist["data"]
    
        #It connects to the API with the Blacklist function and if it cannot be done, an error message will be sent.

    except Exception as e:
        logging.error("Hubo error con la APIKEY ya que no contesto la API")
        print("Hubo un error al conectarse con la API", e)
        exit()
    
    else:
        logging.info("Con un ciclo for se obtienen todas las ips sospechosas")
        for i in range(len(len_blacklist)):
            querystring_check={
            'ipAddress': r_json_blacklist["data"][i]["ipAddress"],
            'maxAgeInDays': '90'}
    
            #Suspicious IPs are being checked

            try:
                logging.info("Se conecta con la API en cuanto a la Blacklist")
                r_check=requests.get(url_check, headers=headers_check, params=querystring_check)
                r_json_check=r_check.json()
    
                #connects with the check function of the API

            except Exception as e:
                logging.error("Hubo error con la APIKEY ya que no contesto la API")
                print("Hubo un error con la al conectarse a la api desde la ip",\
                    r_json_blacklist["data"][i]["ipAddress"], "\n", e)
                
            else:

                if i==0:
                    file_name=Name
                    with open(file_name, "w") as file:
                        file.write("El ip sospechoso es:"+str(r_json_blacklist["data"][i]["ipAddress"]))
                        if "totalReports" in r_json_check["data"]:
                            file.write("Se reportó esta IP por:"\
                                    +str(r_json_check["data"]["totalReports"]))
                            file.write("La IP sospechosa es del país(codigo):"\
                                    +str(r_json_check["data"]["totalReports"]))
                            file.write("La puntuacion que tiene al abuso de confianza es: "\
                                +str(r_json_check["data"]["abuseConfidenceScore"])+"\n")
                        else:
                            file.write("No se encontraron reportes recientes para esta IP.\n")
                        file.write("-"*50)                            

                try:
                    logging.info("Se intenta crear el archivo")
                    file=open(file_name, "a")
                    file.write("El ip sospechoso es:"+str(r_json_blacklist["data"][i]["ipAddress"]))
                    if "totalReports" in r_json_check["data"] :
                        file.write("Se reportó esta IP por:"\
                                   +str(r_json_check["data"]["totalReports"]))
                        file.write("La IP sospechosa es del país(codigo):"\
                                   +str(r_json_check["data"]["totalReports"]))
                        file.write("La puntuacion que tiene al abuso de confianza es: "\
                              +str(r_json_check["data"]["abuseConfidenceScore"])+"\n")
                    else:
                        file.write("No se encontraron reportes recientes para esta IP.\n")
                    file.write("-"*50+"\n")
                    file.close()
            
                    #The output of the suspicious IP is saved in a file

                except Exception as e:
                    logging.error("Hubo un error al crear el archivo")
                    print("Hubo un error al crear el archivo", e)  
    finally:
        print("Se termino de ejecutar la funcion")
