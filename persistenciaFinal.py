import paho.mqtt.client as mqtt

from modelDB import insertarobservacion
import json
from graficar import plotear
from colores import *
from mylibreria import Device

import logging

logging.basicConfig(level=logging.INFO)

# copy graph
import shutil

import sys

# Ploteamos cuando se cumplen las condiciones

# Por el momento la funcionalidad es basica
#   - Escuchar las observaciones del Device hacia todas las APS
#   - Cuando se cumple que existen almenos 3 APs disponibles, se genera una estimación
#   - La estimación se plotea en una imagen tipo mapa donde se pone la ubicacion estimada del Dispositivo
#   - Una web basica refresca la imagen generada

# TODO
#   - Actualizar el codigo de los ESP_32 para incluid IMEI ✅
#   - Poder gestionar las observaciones de cada unos de los dispositivos ✅
#       - Añadir observacion para el dispositivo n ✅
#       - Eliminar observaciones viejas (ejemplo: >20s) ✅
#       - Al cumplir condición de triangulación: estimar Locacizacion con la observacion mas reciente de los APs ✅
#       - Al cumplir condición de triangulación: estimar Localizacion con las observaciones mas reciente y no expirada de los APs
#       - 
#   - Poder realizar estimacinones con n Dispositivos ✅
#   
#   - Crear un registro que pueda servirnos para generar el Mapa en el Frontend 
#   - Modificar la Base de datos:
#       - Incluir observaciones ✅
#       - Incluir una tabla de dispositivos ✅
#       - Incluir una tabla de locations (estimaciones) ✅
#       - Registrar Localización de un dispositivo ✅
#       - GENERAR Base de datos limpia con sqlite3 de python ❌
#
#   - Incluir ultima actualización para service.py (antes persistencia.py)
#       - Obtener una observación ✅
#       - Si cumple triangulación genera estimacion para ese dispositivo ✅
#       - Crea un registro de localizacion para ese dispositivo ✅

#   - FrontEnd: Generar Mapa ❌✅
#       - Generar mapa de dispositivos (ultimas localizaciones) ❌
#       - Generar un mapa dada una lista de dispositivos ❌
#   - Probar en el VPS de Jhose ❌ 
#   - Descargar DB Browser for Sqlite ✅

def plotear(x,y,plt):
    
    _x = [0,360,360,0,int(x)]
    _y = [355,355,0,0,int(y)]
    n=['AP1','AP2','AP3','AP4','Device']
    fig, ax = plt.subplots()
    ax.scatter(_x, _y)

    for i, txt in enumerate(n):
        ax.annotate(txt, (_x[i], _y[i]))
    from datetime import datetime
    
    plt.title(f"Hora: {datetime.now()}")
    
    try:
        plt.savefig('grafica_original.png')
        
        shutil.copyfile('grafica_original.png', 'grafica.png')
        
    except Exception as e:
        print(e)

    del plt

# Enlazamos con el broker y guardamos las observaciones en la base de datos
# Connection success callback
def verificar(contador:int):
    if contador==4:
        return True
    else:
        False


def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('hello/world')

def isInDevices(device:str, listaDevice:list)->bool:
    
    logging.debug(f"device: {device}, is in listaDevice: {listaDevice}?")
    for _ in listaDevice:
        if device == _.imei:
            return True
        
    return False

Devices = []
# Message receiving callback


trackingDispositivo = sys.argv[0]

def on_message(client, userdata, msg):
    
    #Devices
    
    conditionToTriangule = False    
    
    # Cada vez que llege un mensaje de una AP -> guardamos la observacion en la base datos
    
    
    # El payload es el contenido del mensaje volcado en el topico "testtopic/observacionesAP"
    
    # Se presupone un bytearray
    
    mensajeJSON = json.loads(str(msg.payload,encoding='utf-8'))
    observacion = mensajeJSON['observacion']
    
    if not isInDevices(observacion['imei'], Devices):
        
        logging.debug(f"not in devices: {observacion['imei']}")
        logging.debug(f"Registering: {observacion['imei']}")
        
        Devices.append(Device(observacion['imei']))
    
    #logging.info(f"Number of devices: {len(Devices)}")
    
    for _ in Devices:
            
        #logging.info(f"{_}, Device: {_.imei}, listaAPs len: {len(_.listaAPs)}")
        
        if _.imei == observacion['imei']:
            
            #if trackingDispositivo in _.imei:
            
            logging.debug(f"Adding new observacion: {observacion} in listaAPs Actual:{_.listaAPs}")
            
            _.addObservation(observacion)
            
            _.refresh()
        
        #if trackingDispositivo in _.imei:
        #    for obs in _.listaAPs:
                
        #        logging.info(f"{obs['nombre']}, {obs['fecha']}\trssi:{obs['rssi']},\tpotencia: {obs['potencia']}")
            
    

    
    

client = mqtt.Client()

# Specify callback function
client.on_connect = on_connect
client.on_message = on_message

# Establish a connection
client.connect('18.229.218.58', 1883, 6000)

# loop
client.loop_forever()