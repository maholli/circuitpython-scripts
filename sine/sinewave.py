import time
import array
import math
import audioio
import board

FREQUENCY = 8000 
SAMPLERATE = 100000 

length = SAMPLERATE // FREQUENCY
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / 18) * (2 ** 15) + 2 ** 15)

audio = audioio.AudioOut(board.A0)
sine_wave_sample = audioio.RawSample(sine_wave,sample_rate=SAMPLERATE)
 
audio.play(sine_wave_sample, loop=True)  # keep playing the sample over and over

a=0
while True:
   a+=1 

