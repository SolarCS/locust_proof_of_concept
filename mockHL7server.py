#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import time
from socket import socket, AF_INET, SOCK_STREAM
import threading

buffsize = 2048

def tcplink(sock, addr):
    # print 'Accept new connection from %s:%s...' % addr
    while True:
        try:
            # data = sock.recv(buffsize)
            data = sock.recv(buffsize).decode()

            if not data:
                break

            print('received data: ' + data)

            # Respond with a mocked response
            sock.send(b"\x0bMSH|^~&|LABADT|DH|EPICADT|DH|201301011228||ACK^A08^ACK|HL7ACK00001|P|2.3\x0dMSA|AA|HL7MSG00001\x1c\x0d")
        except Exception as e:
            print(str(e))
            break
    sock.close()

def main():
    host = ''
    port = 2575

    ADDR = (host,port)

    tctime = socket(AF_INET,SOCK_STREAM)
    tctime.bind(ADDR)
    tctime.listen(3)

    print('Wait for connection ...')
    while True:
        sock,addr = tctime.accept()

        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()

if __name__=="__main__":
    main()