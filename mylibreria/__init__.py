from datetime import datetime
import matplotlib.pyplot as plt
from graficar import plotear
import logging
from modelDB import insertarLocalizacion

from colores import *
class Device():
    
    imei        = None
    listaAPs    = []
    X           = None
    Y           = None
    
    diff = []
        
    medians = {}
    distanciaX = {}
    distanciaY = {}
    
    logger = logging.getLogger(__name__)
    
    def __init__(self,imei:str):
        
        self.imei = imei
        self.listaAPs = []
        self.logger.info(f"listaAP CONSTRUCTOR:{self.listaAPs}")
        pass
    
    def isInListaAPs(self, vertice:str)->bool:
    
        for _ in self.listaAPs:
            if vertice in self.listaAPs:
                return True
            
        return False
    
    def addObservation(self,obs:dict):
        
        """_summary_
            
        Args:
            obs (dict): _description_
            {'imei': 'fasfaf11', 'nombre': 'vertice3', 'x': 360, 'y': 0, 'rssi': -51, 'potencia': 28.18383026, 'distancia': 5.308844566}
        
        """
        AP = obs['nombre']
        
        if not self.isInListaAPs(AP):
            
            obs['fecha'] = datetime.now()
            self.listaAPs.append(obs)
            self.logger.debug("Añadiendo observacion de AP\n\t",obs)
        
        self.logger.debug(f"Device IMEI: {self.imei}: listaAPs: {len(self.listaAPs)}")
        
    def getLocation(self):

        
        
        for _ in self.listaAPs:
            if not _['nombre'] in self.diff:
                self.diff.append(_['nombre'])
            
            if self.medians.get(_['nombre'])!=None:
                self.medians[_['nombre']] = (self.medians[_['nombre']] + _['distancia'])/2
            else:
                self.medians[_['nombre']] = _['distancia']
        
            if self.distanciaX.get(_['nombre'])!=None:
                self.distanciaX[_['nombre']] = (self.distanciaX[_['nombre']] + _['x'])/2
            else:
                self.distanciaX[_['nombre']] = _['x']
            
            if self.distanciaY.get(_['nombre'])!=None:
                self.distanciaY[_['nombre']] = (self.distanciaY[_['nombre']] + _['y'])/2
            else:
                self.distanciaY[_['nombre']] = _['y']
        
        self.logger.debug(f"diff: {self.diff}")
        # Medianas de las distancias
        self.logger.debug(f"medians: {self.medians}")
        
        #Cogemos la distancia de cada AP hacia el movil
        #AP1 = [observacion['nombre'],float(observacion['distancia']),float(observacion['x']),float(observacion['y']),float(observacion['rssi'])]
        
        # Por ejemplo en el dict tenemos self.medians['vertice1'] : distancia
        
        s = 0
        # total
        # sumatoria de distancias AP a movil
        for _ in self.medians:
            # _ -> _['vertice1'] : distancia
            value = self.medians[_]
            s = s + value
        
        # parcial adimensional
        p = {}
        for _ in self.medians:
            
            p.update(
                {
                    
                    _ : float(self.medians[_])/s}
                )
        
        x = 0
        y = 0
        
        for key in self.medians:
            
            x += p[key]*self.distanciaX[key]
            y += p[key]*self.distanciaY[key]
        
        self.logger.info(f"Location: X: {x}. y: {y}")
        plotear(x,y,plt,self.imei)
        insertarLocalizacion(self.imei,x,y)
        
        
    def refresh(self):
        
        self.getLocation()
        
        fechaActual = datetime.now()
        
        tmpObs = self.listaAPs
        
        for observation in self.listaAPs:
            
            delta = fechaActual - observation['fecha']
            
            if (delta.total_seconds()) >= 20:
                tmpObs.remove(observation)
                self.logger.debug(f"[{self.imei}] {FAIL}Eliminando observacion\n\t {ENDC}",observation)

        self.listaAPs = tmpObs
        
        