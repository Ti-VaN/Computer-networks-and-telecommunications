import socket
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, rfft

SERVER_ADDRESS = ('localhost', 8686)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(10)
print('server is running, please, press ctrl+c to stop')

binary_sequence = "000011110110011101111110010100000100100110010111"
fs = 10000
time = np.arange(np.ceil(fs)) / fs
dx = []
dy = []
signals = []
phase = []
j = 0
x = []
for i in range(0, fs * len(binary_sequence)):
    x.append(i * 0.0001)
for i in range(0, len(binary_sequence) - 1, 6):
    dx.append(1 / np.sqrt(42) * ((1 - 2 * int(binary_sequence[i])) * (
            4 - (1 - 2 * int(binary_sequence[i + 2])) * (2 - (1 - 2 * int(binary_sequence[i + 4]))))))
    dy.append(1 / np.sqrt(42) * ((1 - 2 * int(binary_sequence[i + 1])) * (4 - (1 - 2 * int(binary_sequence[i + 3]))) * (
            2 - (1 - 2 * int(binary_sequence[i + 5])))))
    if dx[j] < 0:
        if dy[j] < 0:
            phase.append(5 * np.pi / 4)
        else:
            phase.append(3 * np.pi / 4)
    else:
        if dy[j] < 0:
            phase.append(7 * np.pi / 4)
        else:
            phase.append(np.pi / 4)
    j += 1

for i in range(0, len(phase)):
    signals.append(np.sin(2 * np.pi * time + phase[i]))

signalSum = 0
for i in range(len(signals)):
    signalSum = signalSum + signals[i]

signalFFT = np.fft.fft(signalSum)
signalFFTabs = 2 * np.abs(signalFFT) / fs

# График: сигнал во времени
plt.subplot(1, 1, 1)
plt.plot(time, signalSum)
plt.show()

while True:
    connection, address = server_socket.accept()
    print("new connection from {address}".format(address=address))

    data = connection.recv(1024)
    print(data)

    connection.send(bytes(signalFFTabs))

connection.close()