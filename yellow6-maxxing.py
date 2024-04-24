import wave
import numpy as np


# The way I converted the ith occurrence of the wave
# to what it was representing. I was testing out all the
# possible variations, until this one gave me a readable flag.
def remap(i):
    if i == 0:
        return 1
    if i == 1:
        return 0
    if i == 2:
        return 2
    if i == 3:
        return 3


# Reading the wave file and converting its data points into 16-bit signed integers.
reader = wave.open("yellow6-maxxing.wav", "rb")
data = reader.readframes(-1)
reader.close()
data = np.fromstring(data, np.int16)

# Collecting all the unique waves, then collecting their index in the "unique" array in the "data2" array,
# while remapping them to a different number. I could rewrite this to be a lot better, but I want to
# keep the logic of the script as it was when I solved the problem.
freq = 40
data2 = []
unique = []

for i in range(0, len(data)-80, freq):
    s = data[i:i+40]
    b = True
    v = 0
    for j in range(len(unique)):
        u = unique[j]
        if np.array_equal(u, s):
            b = False
            data2.append(remap(j))
            break
    if b:
        unique.append(s)
        data2.append(remap(len(unique)-1))

# Then taking their binary representation, concatenate them into 8-bit integers, then
# converting them to chars. (mapping them into ASCII)
msg = ""
for i in range(0, len(data2)-6, 4):
    b = data2[i]
    for j in range(1, 4):
        b = b << 2
        b = b | data2[i+j]
    msg += chr(b)

print(msg)


