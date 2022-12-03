import librosa
from paho.mqtt import client as mqtt_client
from scipy.io.wavfile import write
import json
import time

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic = "daniel"
topic1 = "something"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client()       
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#def record(client):
#    print('Recording')
#    fs = 32000  # Frequencia de amostragem
#    seconds = 5  # Duaracao da gravacao
    
#    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
#    sd.wait()
#    write('grav1.wav', fs, recording)
#    print('Done Recording')
#    y, sr = librosa.load('grav1.wav') 
#    yy = y.tolist()
#    df = json.dumps(yy)

def publish(client):
    y, sr = librosa.load('grav1.wav') 
    yy = y.tolist()
    df = json.dumps(yy)
    msg = df
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Message sent to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
        
def subscribe(client: mqtt_client):
    def on_message(client, userdata, start):
        print(f"Received start from `{start.topic1}` topic")
        inicio = (start.payload.decode('utf-8'))
        if inicio == 'start':
            publish(client)

    client.subscribe(topic1)
    client.on_message = on_message
        
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()