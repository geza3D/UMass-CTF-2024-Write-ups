import wave
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf


# A sample length of 50000 with lags ranging from 0 to 50000 makes the repeating pattern pretty obvious,
# while not taking forever to calculate.
def plotAcf(data):
    plot_acf(x=data[:50001], lags=50000)
    plt.show()


# Reading the wave file and converting its data points into 16-bit signed integers.
reader = wave.open("yellow5-maxxing.wav", "rb")
data = reader.readframes(-1)
reader.close()
data = np.fromstring(data, np.int16)

# We split up the data into arrays with the length of the sampleSize, then
# take the average of each index. I do this to try getting rid of the noise.
# I got the sample size using the plot_acf function of statsmodels.
# The plotAcf(data) function plots the autocorrelation for those who are interested.
plotAcf(data)
baseSample = 11160
baseSampleMult = 1
sampleSize = baseSample * baseSampleMult

sampler = [0] * sampleSize
c = 0

for i in range(0, len(data) - sampleSize, sampleSize):
    sample = data[i:i + sampleSize]
    sampler += sample
    c += 1

for i in range(0, len(sampler)):
    sampler[i] /= c

sampler = [1 if x > 0 else 0 for x in sampler]

# We now find the unique sequenced of 1s and 0s, and take their index as our new sequence
# (since there's only two of them).
# Even though, I could swap out the code here to something a lot better
# I'm going to leave it like this since this is how I got my answer, I want to keep
# the core of the logic used intact.
data2 = []
unique = []

for i in range(0, len(sampler), 31):
    s = sampler[i:i + 31]
    b = True
    v = 0
    for j in range(len(unique)):
        u = unique[j]
        if np.array_equal(u, s):
            b = False
            data2.append(j)
            break
    if b:
        unique.append(s)
        data2.append(len(unique) - 1)

# Then taking their binary representation, concatenate them into 8-bit integers, then
# converting them to chars. (mapping them into ASCII)
# Funnily enough, the signal doesn't actually start with the message,
# but it's not that hard to find the start of it.
msg = ""
for i in range(0, len(data2), 8):
    b = data2[i]
    for j in range(1, 8):
        b = b << 1
        b = b | data2[(i + j)]
    msg += chr(b)

print(msg)
