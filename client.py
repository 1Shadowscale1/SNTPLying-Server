#!/usr/bin/env python
import socket
import time
from ntplib import NTPStats

def launch():
    st = NTPStats()
    s = socket.socket()
    s.connect(('localhost', 123))
    s.send(str('HLO').encode())
    d = s.recv(1024)
    s.close()
    print('Received data: {}'.format(d))
    st.from_data(d)
    print('Time gotten by user: {}'.format(time.ctime(st.tx_time)))


if __name__ == "__main__":
    launch()