#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import socket
import subprocess
import sys


HOST = '127.0.0.1'
PORT = 9999

SET_VOLUME_LEVEL = "amixer -D pulse sset Master {}%"
GET_VOLUME_LEVEL = ("amixer -D pulse get Master "
    "| awk -F 'Left:|[][]' 'BEGIN {RS=\"\"}{ print $3 }'")
# GET_CPU_USAGE = ("top -b -n2 | grep \"Cpu(s)\" " 
#     "| awk '{print $2+$4 \"%\"}' | tail -n1")

GET_CPU_USAGE = ("grep 'cpu ' /proc/stat "
    "| awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage \"%\"}'")
GET_MEMORY_USAGE = "free | grep Mem | awk '{print $3/$2*100}'"


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
        try:
            self.sock.bind((self.host, self.port))
        except OSError:
            print("Socket juz istnieje")
            sys.exit(1)

        self.sock.listen()
        conn, addr = self.sock.accept()

        subprocess.call(SET_VOLUME_LEVEL.format(0), shell=True)

        with conn:
            print("Connected by {}".format(addr))

            while True:
                header = conn.recv(1)
                header = header.decode()
                #print("Header: {}".format(header))

                if header == '1':
                    data = conn.recv(1)
                    self._shortcut_buttons(data)

                elif header == '2':
                    msg_len = int(conn.recv(1))
                    data = conn.recv(msg_len)
                    self._adjust_volume_level(data)

                elif header == '3':
                    data = self._get_volume_level()
                    #print("Dane: {}".format(data))
                    msg_len = str(len(data))
                    conn.sendall(msg_len.encode("utf-8"))
                    conn.sendall(data)

                elif header == '4':
                    data = self._get_cpu_usage()
                    #print("Dane: {}".format(data))
                    msg_len = str(len(data))
                    conn.sendall(msg_len.encode("utf-8"))
                    conn.sendall(data)

                elif header == '5':
                    data = self._get_memory_usage()
                    #print("Dane: {}".format(data))
                    msg_len = str(len(data))
                    conn.sendall(msg_len.encode("utf-8"))
                    conn.sendall(data)

                if not header:
                    break

    def _shortcut_buttons(self, data):
        data = int(data)
        try:
            subprocess.call(Host.commands[data], shell=True)
        except KeyError:
            pass

    def _adjust_volume_level(self, data):
        #print("Volume level {}".format(data.decode()))
        subprocess.call(SET_VOLUME_LEVEL.format(data.decode()), shell=True)

    def _get_volume_level(self):
        pipe = subprocess.Popen(
            GET_VOLUME_LEVEL, shell=True, stdout=subprocess.PIPE).stdout
        value = pipe.read()
        value = value.strip()
        value = value[:len(value)-1]
        return value

    def _get_cpu_usage(self):
        pipe = subprocess.Popen(
            GET_CPU_USAGE, shell=True, stdout=subprocess.PIPE).stdout
        value = pipe.read()
        value = value.strip()[:5]
        return value

    def _get_memory_usage(self):
        pipe = subprocess.Popen(
            GET_MEMORY_USAGE, shell=True, stdout=subprocess.PIPE).stdout
        value = pipe.read()
        value = value.strip()[:5]
        return value


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        Host(s, HOST, PORT).loop()

if __name__ == "__main__":
    main()

