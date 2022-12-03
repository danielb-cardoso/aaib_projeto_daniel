from paho.mqtt import client as mqtt_client
import streamlit as st
import librosa
import matplotlib.pyplot as plt
from librosa import display
import numpy as np

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

st.title('Extração de Features de um ficheiro áudio')

if st.button('Start'):        
    publish(client)

if st.button('Extração'):
    
    st.header('Extração de Features')
    dados=np.loadtxt(r'new_msg.csv', delimiter=',', dtype='str' )
    y = np.asarray(dados, dtype=np.float64)
    sr=22050

    # espetrograma
    st.subheader('Espectograma')
    
    X = librosa.stft(y)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(15, 3))
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    
    # Magnitude total do sinal (sonoridade / parametro de energia)
    st.subheader('Sonoridade')
    
    # Valor de RMS para cada valor de magnitude
    S, phase = librosa.magphase(librosa.stft(y)) #frequencia e fase
    rms = librosa.feature.rms(S=S) #root mean square da gravacao
    
    # Grafico
    fig, ax = plt.subplots(figsize=(15, 6), nrows=2, sharex=True)
    times = librosa.times_like(rms)
    ax[0].semilogy(times, rms[0], label='Energia RMS')
    ax[0].set(xticks=[])
    ax[0].legend()
    ax[0].label_outer()
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                             y_axis='log', x_axis='time', ax=ax[1])
    ax[1].set(title='Espetrograma da Magnitude logarítmico')
    st.pyplot()
    
    #zero crossing rate
    st.subheader('Zero Crossing Rate')
    
    zcrs = librosa.feature.zero_crossing_rate(y)
    print(f"Zero crossing rate: {sum(librosa.zero_crossings(y))}")
    plt.figure(figsize=(15, 3))
    plt.plot(zcrs[0])
    plt.title('Zero Crossing Rate')
    st.pyplot()