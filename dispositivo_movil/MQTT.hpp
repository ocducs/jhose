#pragma once

//Defino la ip del broker mqtt
const IPAddress MQTT_HOST(18, 229, 218, 58);
const int MQTT_PORT = 1883;

AsyncMqttClient mqttClient;

String GetPayloadContent(char* data, size_t len)
{
  String content = "";
  for(size_t i = 0; i < len; i++)
  {
    content.concat(data[i]);
  }
  return content;
}

void SuscribeMqtt()
{
  uint16_t packetIdSub = mqttClient.subscribe("hello/world", 0);
  Serial.print("Subscribing at QoS 2, packetId: ");
  Serial.println(packetIdSub);
}
/*
String payload;
void PublishMqtt(String data)
{
  String payload = data;
  mqttClient.publish("hello/world", 0, true, (char*)payload.c_str());
}
*/
void PublishMqtt(StaticJsonDocument<300> data)
{
  String payload = "";

  serializeJson(data, payload);

  mqttClient.publish("hello/world", 0, true, (char*)payload.c_str());
}

void OnMqttReceived(char* topic, char* payload, AsyncMqttClientMessageProperties properties, size_t len, size_t index, size_t total)
{
  Serial.print("Received on ");
  Serial.print(topic);
  Serial.print(": ");

  String content = GetPayloadContent(payload, len);

  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, content);
  if(error) return;

  unsigned long data = doc["data"];
  Serial.print("Millis:");
  Serial.println(data);
}
/*
void OnMqttReceived(char* topic, char* payload, AsyncMqttClientMessageProperties properties, size_t len, size_t index, size_t total)
{
  Serial.print("Received on ");
  Serial.print(topic);
  Serial.print(": ");

  String content = GetPayloadContent(payload, len);
  Serial.print(content);
  Serial.println();
}*/
