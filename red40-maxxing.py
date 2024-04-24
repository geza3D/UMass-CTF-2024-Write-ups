import wave
import numpy as np

# Reading the wave file and converting its data points into 16-bit signed integers.
reader = wave.open("red40-maxxing.wav", "rb")
data = reader.readframes(-1)
data = np.fromstring(data, np.int16)
reader.close()

# Converting to ones and zeros. 
# One meaning that the amplitude is positive, zero meaning that the amplitude is negative.
data = [1 if x > 0 else 0 for x in data if x != 0]


# Then taking those 1s and 0s and concatenating them into 8-bit integers, then converting that
# to chars (mapping them into ASCII)
msg = ""
for i in range(0, len(data), 8):
    b = data[i]
    for j in range(1, 8):
        b = b << 1
        b = b | data[i+j]
    msg += chr(b)

print(msg)


