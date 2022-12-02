from paho.mqtt import client as mqtt_client
import time
import csv
import json
import pandas as pd

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic = "daniel"

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received data from `{msg.topic}` topic")
        data = (msg.payload.decode('utf-8'))
        for i in range (2):
            try:
                df = pd.read_json(r'C:\Users\ASUS\Desktop\MEB\2 ano\1 semestre\AAIB\projeto_alternativo\msg.json') 
                df.to_csv(r'C:\Users\ASUS\Desktop\MEB\2 ano\1 semestre\AAIB\projeto_alternativo\new_msg.csv', encoding='utf-8', index=False)        
            except Exception:
                with open (r'C:\Users\ASUS\Desktop\MEB\2 ano\1 semestre\AAIB\projeto_alternativo\msg.json','w') as file:
                    file.write(data)

    client.subscribe(topic)
    client.on_message = on_message
        
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    client.loop_stop()

if __name__ == '__main__':
    run()