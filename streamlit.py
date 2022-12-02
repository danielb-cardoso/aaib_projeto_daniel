from paho.mqtt import client as mqtt_client
import streamlit as st
import librosa
import matplotlib.pyplot as plt
from librosa import display

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic = "daniel" 

client = mqtt_client.Client()
client.connect(broker, port)

def publish(client):
    inicio = 'start'
    result = client.publish(topic, inicio)
    status = result[0]
    if status == 0:
        print(f"Message sent to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
        
publish(client)