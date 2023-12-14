import paho.mqtt.client as mqtt

from modelDB import insertarobservacion
import json
from graficar import plotear
from colores import *
import mylib
# copy graph
import shutil

AP1 = None
AP2 = None
AP3 = None
AP4 = None

# Ploteamos cuando se cumplen las condiciones

# Por el momento la funcionalidad es basica
#   - Escuchar las observaciones del Device hacia todas las APS
#   - Cuando se cumple que existen almenos 3 APs disponibles, se genera una estimación
#   - La estimación se plotea en una imagen tipo mapa donde se pone la ubicacion estimada del Dispositivo
#   - Una web basica refresca la imagen generada

# TODO
#   - Actualizar el codigo de los ESP_32 para incluid IMEI ✅
#   - Poder realizar estimacinones con n Dispositivos ❌
#   - Crear un registro que pueda servirnos para generar el Mapa en el Frontend 
#   - Modificar la Base de datos:
#       - Incluir observaciones ✅
#       - Incluir una tabla de dispositivos ✅
#       - Incluir una tabla de locations (estimaciones) ✅
#   - Incluir ultima actualización para service.py (antes persistencia.py)
#       - Obtener una observación
#       - Si cumple triangulación genera estimacion para ese dispositivo
#       - Crea un registro de localizacion para ese dispositivo

#   - FrontEnd: Generar Mapa
#       - Generar mapa de dispositivos (ultimas localizaciones)
#       - Generar un mapa dada una lista de dispositivos
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
    
    for _ in listaDevice:
        if device == _['imei']:
            return True
        
    return False
    
# Message receiving callback
def on_message(client, userdata, msg):
    
    #Devices
    Devices = []
    
    
    # Cada vez que llege un mensaje de una AP -> guardamos la observacion en la base datos
    global AP1, AP2, AP3, AP4
    
    # El payload es el contenido del mensaje volcado en el topico "testtopic/observacionesAP"
    
    # Se presupone un bytearray
    RC = str(msg.payload,encoding='utf-8')
    
    conditionToTriangule = False
    
    
    #try:
    mensajeJSON = json.loads(RC)
    observacion = mensajeJSON['observacion']
    
    if isInDevices(observacion['imei'], Devices):
        
        Devices.append(mylib(observacion))
        
    for _ in Devices:
        
        if _['imei'] == observacion['imei']:
            
            _.addObservation(observacion)
            
            _.refresh()

    insertarobservacion(imei=observacion['imei'],
                        hostname=observacion['nombre'],
                        power=observacion['distancia'],
                        rssi=observacion['rssi'],
                        x=observacion['x'],
                        y=observacion['y'])
    
    if '1' in observacion['nombre']:
        AP1 = [observacion['nombre'],float(observacion['distancia']),float(observacion['x']),float(observacion['y']),float(observacion['rssi'])]
    if '2' in observacion['nombre']:
        AP2 = [observacion['nombre'],float(observacion['distancia']),float(observacion['x']),float(observacion['y']),float(observacion['rssi'])]
    if '3' in observacion['nombre']:
        AP3 = [observacion['nombre'],float(observacion['distancia']),float(observacion['x']),float(observacion['y']),float(observacion['rssi'])]
    if '4' in observacion['nombre']:
        AP4 = [observacion['nombre'],float(observacion['distancia']),float(observacion['x']),float(observacion['y']),float(observacion['rssi'])]
   
    cont =  0 

    if AP1 != None:
        cont+=1
    if AP2 != None:
        cont+=1
    if AP3 != None:
        cont+=1
    if AP4 != None:
        cont+=1  

    print(f'{OKCYAN}Numero de APs para triangular:{ENDC} {cont}')

    conditionToTriangule = verificar(cont)
    

    if conditionToTriangule:
        
        # IMplementacion de codigo de triangulacioin simple

        def calcular():
            p0,p1,p2,p3 = None,None,None,None
            p = []
            s = 0
            misAps = [AP1,AP2,AP3,AP4]
            
            print(f"""
    {OKBLUE}Dispositivos Fijos APS{ENDC}:""")
            for _ in misAps:
                print(f"""
        {OKCYAN}nombre{ENDC}:\t{_[0]}
            x:\t\t{_[2]}
            y:\t\t{_[3]}
            rssi:\t{_[4]}
            potencia:\t{_[1]}
            
                """)
                s = s + float(_[1])
                
            for _ in misAps:
                p.append(float(_[1])/s)
            
            
            #X = p[0] *  (AP1-> x)  + p[1] *    (AP2-> x) + p[2] *  (AP2-> x)   + p[3] *  (AP4-> x)
            X = p[0] * misAps[0][2] + p[1] * misAps[1][2] + p[2] * misAps[2][2] + p[3] * misAps[3][2]
            #y = p[0] *  (AP1-> y)  + p[1] *    (AP2-> y) + p[2] *  (AP2-> y)   + p[3] *  (AP4-> y)
            Y = p[0] * misAps[0][3] + p[1] * misAps[1][3] + p[2] * misAps[2][3] + p[3] * misAps[3][3]
            return X,Y

            intertarLocalizacion()

        import matplotlib.pyplot as plt
        print(f"{WARNING}[Warning]{ENDC}Tratando de enviar ploteo")

        #Coordenadas calculadas:
        x,y = calcular()
        print(f"{OKGREEN}[PASSED]{ENDC} Enviando coordenadas trianguladas: {OKYELLOW}[{x}, {y}]{ENDC}")
        
        # añadir dispositivo al mapa
        #plotear(x,y,plt)
    

client = mqtt.Client()

# Specify callback function
client.on_connect = on_connect
client.on_message = on_message

# Establish a connection
client.connect('18.229.218.58', 1883, 6000)

# loop
client.loop_forever()