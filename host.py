#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 9999

class Host(object):
    def __init__(self, s, host, port):
        self.s = s
        self.host = host
        self.port = port

    def loop(self):
        self.s.bind((self.host, self.port))
        self.s.listen()
        conn, addr = self.s.accept()
        with conn:
            print("Connected by {}".format(addr))
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)


def main():
    #Host().loop()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        Host(s, HOST, PORT).loop()

if __name__ == "__main__":
    main()

