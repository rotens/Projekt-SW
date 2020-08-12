#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import subprocess

def main():
    subprocess.Popen("python3 host.py", shell=True)
    subprocess.Popen("python3 evb.py", shell=True).wait()

if __name__ == "__main__":
    main()