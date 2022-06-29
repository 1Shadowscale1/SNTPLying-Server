#!/usr/bin/env python
import struct
import ntplib
import socket
import time

TIMEOF1970YEAR = 2208988800

def read_conf():
    try:
        with open('conf.txt') as conf_file:
            fake_shift = int(conf_file.readline())
            return fake_shift
    except Exception as e:
        print('Error occured: {}'.format(e))
    finally:
        print('Setted shift time: {} seconds'.format(fake_shift))


def launch(fake_shift):
    ntp = ntplib.NTPClient()
    s = socket.socket()
    s.bind(('', 123))
    s.listen(1)
    connection, address = s.accept()
    print('connected:', address)
    while True:
        d = connection.recv(1024)
        if d:
            req = ntp.request('ntp3.stratum2.ru')
            truet = req.tx_time
            d = req.to_data()
            db = bytearray(d)
            newtd = struct.pack('!1I', TIMEOF1970YEAR + int(truet) + fake_shift)
            newtdb = bytearray(newtd)
            print(newtdb)
            db[40:43] = newtdb
            req.from_data(db)
            print('Time: {}'.format(time.ctime(truet)) + '\n' + \
                'Time with setted shift: {}'.format(time.ctime(req.tx_time)))
            connection.send(db)
        else:
            break
    connection.close()


if __name__ == "__main__":
    fake_shift = read_conf()
    launch(fake_shift)