from classes import Lorenz
from classes import Protocol
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import cv2
import math
import numpy as np
import pyaudio
import time

CHUNK = 3000 # number of data points to read at a time
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

print sender.get_sequence(1)
print receiver.get_sequence(1)
# create a numpy array holding a single read of audio data
while True: #to it a few times just to see
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    print data
    start_time = time.time()
    encrypt_sound = sender.encrypt(data.copy())
    print encrypt_sound
    print("--- Encrypt %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    decrypt_sound = receiver.decrypt(encrypt_sound.copy())
    print decrypt_sound
    print("--- Decrypt %s seconds ---" % (time.time() - start_time))
