from classes import Lorenz
from classes import Protocol
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
#import cv2
import math
import numpy as np
import pyaudio
import time

CHUNK = 1024 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              output=True,frames_per_buffer=CHUNK) #uses default input device

master = Lorenz()
slave = Lorenz()

sender = Protocol(master)
receiver = Protocol(slave)

key = sender.get_sequence(25)
receiver.synchronize(key)

def entropia(datos):
    rango = np.max(datos)-np.min(datos)+1
    e =0
    for i in datos:
        p=np.count_nonzero(datos==datos[0])/rango
        e+=(p*math.log(p,2))

    return -e

def correlacion(datos, enc):
    e=datos.sum()/len (datos)
    vx=(((datos-e)**2).sum())/len(datos)
    vk=(((enc-e)**2).sum())/len(enc)
    c=(((datos-e)*(enc-e)).sum())/len(datos)
    return c/(math.sqrt(vx)*math.sqrt(vk))

def ruido(datos, desen):
    x=(datos**2).sum()
    y=((datos-desen)**2).sum()
    return 10*math.log(x/y, 10)


#print sender.get_sequence(1)
#print receiver.get_sequence(1)
# create a numpy array holding a single read of audio data
while True: #to it a few times just to see
    data2 =stream.read(CHUNK)
    data = np.fromstring(data2,dtype=np.int16)
    #stream.write(data)
    print data
    start_time = time.time()
    encrypt_sound = sender.encrypt(data.copy())
    #stream.write(encrypt_sound)
   
    #print encrypt_sound
    print("--- Encrypt %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    decrypt_sound = receiver.decrypt(encrypt_sound.copy())
   
    print decrypt_sound
    stream.write(decrypt_sound)
    print("--- Decrypt %s seconds ---" % (time.time() - start_time))




