#include <ArduinoJson.h>

#include <WiFi.h>
#include <AsyncMqttClient.h>

//Configuración de nuestro esp para wifi y configuración de ip estatica localmente
#include "config.h"

//Incluimos configuracion de nuestro broker ya sea local o online
#include "MQTT.hpp"

//Incluimos algunas utilidades para el wifi como su tipo de conectividad (o bien AP o bien STA)
#include "ESP32_Utils.hpp"

//Incluimos el encabezado que incluye callbacks de wifi y mqtt
#include "ESP32_Utils_MQTT_Async.hpp"

//Usamos "math.h" de arduino standard para sqrt()
#include "math.h"

//Usamos cmath para pow()
#include <cmath>

//Estructura para las APs y metodos
struct AP { //para a
  String nombre;
  float x;
  float y;
  float rssi = 0;
  float potencia = 0;
  float distancia = 0.1;
  
  void getPotencia() {

    //para cada Ap, calcular distancia a Ap(se conoce RSSI y la ubicacion de la AP,
    //y que es inversamente proporcional al cuadrado de la distancia)
    //se sabe que la relacion de Potencia-RSSI
    //
    //        RSSI=10log(PS/PE)
    //
    //PS=Potencia de salida(la real que llega)
    //RSSI=Received Signal Strength Indicator
    //PE=Potencia de entrada (Emitido por el AP)
    //Donde PE es 1mW y se desea conocer PS

    potencia = 10000.0 * pow(10.0, (rssi / 20.0));
  }
  //void getDistancia() {

  //sabiendo que la potencia es inversa al cuadrado de la distancia
  //
  //    Potencia=k/d^2
  //
  //distancia = sqrt(potencia);

  //}
  float getDistancia() {

    //sabiendo que la potencia es inversa al cuadrado de la distancia
    //
    //    Potencia=k/d^2
    //
    distancia = sqrt(potencia);
   
  }
} misAps[4];

void setup()
{
  Serial.begin(115200);
  misAps[0].nombre = "vertice1";
  misAps[0].x = 0;
  misAps[0].y = 355;
  misAps[1].nombre = "vertice2";
  misAps[1].x = 360;
  misAps[1].y = 355;
  misAps[2].nombre = "vertice3";
  misAps[2].x = 360;
  misAps[2].y = 0;
  misAps[3].nombre = "vertice4";
  misAps[3].x = 0;
  misAps[3].y = 0;
  delay(500);

  WiFi.onEvent(WiFiEvent);
  InitMqtt();

  ConnectWiFi_STA();
}
int redesDisponibles;
void loop()
{

  delay(3000);
  int A = WiFi.scanNetworks();

  for (int i = 0; i < 4; i++) {

    String cad = misAps[i].nombre;

    for (int j = 0; j < A ; j++) {

      String B = WiFi.SSID(j);

      if (B.indexOf(cad)!=-1) {

        Serial.println(WiFi.SSID(j));
        Serial.println(WiFi.RSSI(j));
        misAps[i].rssi = WiFi.RSSI(j);

        misAps[i].getPotencia();
        misAps[i].getDistancia();
        
        StaticJsonDocument<300> jsonDoc;
        // dispositivo = IMEI
        jsonDoc["observacion"]["imei"] = "8fa813718";
        jsonDoc["observacion"]["nombre"] = misAps[i].nombre;
        jsonDoc["observacion"]["x"] = misAps[i].x;
        jsonDoc["observacion"]["y"] = misAps[i].y;
        jsonDoc["observacion"]["rssi"] = misAps[i].rssi;
        jsonDoc["observacion"]["potencia"] = misAps[i].potencia;
        jsonDoc["observacion"]["distancia"] = misAps[i].distancia;
        PublishMqtt(jsonDoc);
      }
    }

  }
  
}
