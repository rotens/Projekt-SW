#!/usr/bin/env python3

import os
import socket

HOST = '127.0.0.1'
PORT = 9999

class Host(object):
    commands = {
        0: "firefox",
        1: "vim",
        2: "shutdown now",
        3: "shutdown -r",
        4: "systemctl suspend",
        5: "firefox https://www.github.com",
        6: "firefox https://www.pk.edu.pl",
        7: "firefox https://pl.wikipedia.org/",
    }

    def __init__(self, sock, host, port):
        self.sock = sock
        self.host = host
        self.port = port

    def loop(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        conn, addr = self.sock.accept()
        with conn:
            print("Connected by {}".format(addr))
            while True:
                data = conn.recv(1)
                print(data)
                if data == b'1':
                    data = conn.recv(4)
                    self._shortcut_buttons(data)
                #if not data:
                    #break

    def _shortcut_buttons(self, data):
        data = int(data)
        try:
            os.system(Host.commands[data])
        except KeyError:
            pass

        

def main():
    #Host().loop()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        Host(s, HOST, PORT).loop()

if __name__ == "__main__":
    main()

