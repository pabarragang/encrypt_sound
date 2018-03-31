from classes import Lorenz
from classes import Protocol
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
#import cv2
import math
import numpy as np
import pyaudio
import time

CHUNK = 1000 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

master = Lorenz()
slave = Lorenz()

sender = Protocol(master)
receiver = Protocol(slave)

key = sender.get_sequence(25)
receiver.synchronize(key)
def entropia(datos):
    rango = np.max(datos)-np.min(datos)
    e =0
    for i in datos:
        p=np.count_nonzero(datos==datos[0])/rango
        e+=(p*math.log(p,2))

    return -e



#print sender.get_sequence(1)
#print receiver.get_sequence(1)
# create a numpy array holding a single read of audio data
while True: #to it a few times just to see
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    #print data
    print("max: ", np.amax(data), " min: ", np.amin(data))
    start_time = time.time()
    encrypt_sound = sender.encrypt(data.copy())
    print (entropia(encrypt_sound))
    #print encrypt_sound
    print("max: ", np.amax(encrypt_sound), " min: ", np.amin(encrypt_sound))
    print("--- Encrypt %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    decrypt_sound = receiver.decrypt(encrypt_sound.copy())
    print("max: ", np.amax(decrypt_sound), " min: ", np.amin(decrypt_sound))
    #print decrypt_sound
    print("--- Decrypt %s seconds ---" % (time.time() - start_time))




