# -*- coding: utf-8 -*-
import wave
import pylab as pl
import numpy as np
import cmath
import math


def FFT(data):
  n = len(data)
  if n == 2:
    return [data[0] + data[1], data[0] - data[1]]

  data_even = []
  data_odd = []
  for i in range(n):
    if (i & 1) == 0:
      data_even.append(data[i])
    else:
      data_odd.append(data[i])

  G = FFT(data_even)
  H = FFT(data_odd)
  pi = math.pi
  step = cmath.exp(complex(0, - 2 * pi / n))
  W = 1
  half_n = (int)(n / 2)

  res = [0 for i in range(n)]

  for i in range(half_n):
    res[i] = G[i] + W * H[i]
    res[i + half_n] = G[i] - W * H[i]
    W = W * step
  return res

def IFFT(data):
  n = len(data)
  if n == 2:
    return [data[0] / 2 + data[1] / 2, data[0] / 2 - data[1] / 2]

  data_even = []
  data_odd = []
  for i in range(n):
    if (i & 1) == 0:
      data_even.append(data[i])
    else:
      data_odd.append(data[i])

  G = IFFT(data_even)
  H = IFFT(data_odd)
  pi = math.pi
  step = cmath.exp(complex(0, 2 * pi / n))
  W = 1
  half_n = (int)(n / 2)

  res = [0 for i in range(n)]

  for i in range(half_n):
    res[i] = G[i] / 2 + W * H[i] / 2
    res[i + half_n] = G[i] / 2 - W * H[i] / 2
    W = W * step
  return res



# 打开WAV文档
f = wave.open(r"15307110189-00-01.wav", "rb")

# 读取格式信息
# (nchannels, sampwidth, framerate, nframes, comptype, compname)
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]

#print(nframes)

# 读取波形数据
str_data = f.readframes(nframes)
f.close()

#将波形数据转换为数组
wave_data = np.frombuffer(str_data, dtype=np.short)
#wave_data.shape = -1, 2
wave_data = wave_data.T

#print(wave_data.size)
data = []
for x in wave_data:
  data.append(x)

time = np.arange(0, nframes) * (1.0 / framerate)
#print(wave_data[0])
# 绘制波形
pl.subplot(311) 
pl.plot(time, data)

data = FFT(data)

pl.subplot(312) 
pl.plot(time, data, c="g")

data = IFFT(data)


pl.subplot(313) 
pl.plot(time, data)

pl.xlabel("time (seconds)")
pl.show()
