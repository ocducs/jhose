import paho.mqtt.client as mqtt

#Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    #client.subscribe('testtopic/observacionesAP')
    client.subscribe('hello/world')

# Message receiving callback
def on_message(client, userdata, msg):
    
    print(type(msg.payload))
    
    print(msg.topic,len(msg.payload),str(msg.payload))

client = mqtt.Client()

# Specify callback function
client.on_connect = on_connect
client.on_message = on_message

# Establish a connection
client.connect('18.229.218.58', 1883, 60)
# Publish a message
client.loop_forever()