#!/usr/bin/env python3

import socket
import tkinter as tk

HOST = '127.0.0.1'
PORT = 9999

SCREEN_COLOR = "#0000e6"
SCREEN_TEXT_COLOR = "#A9A9A9"
DIODE_ON_COLOR = "#ff0000" 
DIODE_OFF_COLOR = "#660000"

DIODES_NUM = 8
BUTTONS_NUM = 8

class Evb(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        self.lb_screen = tk.Label(master=self, text="LCD HD44780")
        self.lb_screen.grid(row=0, columnspan=DIODES_NUM)
        self.screen = tk.Frame(master=self, height=25, width=300, bg=SCREEN_COLOR)
        self.screen.grid(row=1, columnspan=DIODES_NUM)
        self.screen.grid_propagate(False)
        self.screen.columnconfigure(1, weight=1)
        self.screen.rowconfigure(0, weight=1)

        self.lb_memory = tk.Label(
            master=self.screen, text="MEM: 100", font=("", 12),
            bg=SCREEN_COLOR, fg=SCREEN_TEXT_COLOR)
        self.lb_cpu = tk.Label(
            master=self.screen, text="CPU: 100", font=("", 12),
            bg=SCREEN_COLOR, fg=SCREEN_TEXT_COLOR)
        self.lb_temperature = tk.Label(
            master=self.screen, text="TEMP: 100", font=("", 12),
            bg=SCREEN_COLOR, fg=SCREEN_TEXT_COLOR)
        self.lb_memory.grid(row=0, column=0)
        self.lb_cpu.grid(row=0, column=1)
        self.lb_temperature.grid(row=0, column=2)

        self.lb_diodes = tk.Label(master=self, text="Diodes")
        self.lb_diodes.grid(row=2, columnspan=DIODES_NUM)

        self.diodes = []
        for i in range(DIODES_NUM):
            self.diodes.append(tk.Frame(master=self))
            self.diodes[i]["width"] = 20
            self.diodes[i]["height"] = 20
            self.diodes[i]["bg"] = DIODE_OFF_COLOR
            self.diodes[i].grid(row=3, column=i, padx=10)

        self.lb_potentiometer = tk.Label(master=self, text="ADC potentiometer", pady=10)
        self.lb_potentiometer.grid(row=4, columnspan=DIODES_NUM)
        self.potentiometer = tk.Scale(master=self, from_=0, to=100, 
        orient=tk.HORIZONTAL, length=300, tickinterval=20)
        self.potentiometer.bind("<Button-1>", self.callback)
        self.potentiometer.grid(row=5, columnspan=DIODES_NUM)

        self.lb_buttons = tk.Label(master=self, text="Shortcuts")
        self.lb_buttons.grid(row=6, columnspan=DIODES_NUM)
        self.buttons = []
        for i in range(BUTTONS_NUM):
            self.buttons.append(tk.Button(master=self))
            self.buttons[i]["text"] = "S{}".format(i)
            self.buttons[i]["width"] = 1
            self.buttons[i]["height"] = 1
            self.buttons[i].grid(row=7, column=i, padx=10)
        
    def callback(self, event):
        print("Test")
                        

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)

# print('Received', repr(data))

def main():
    root = tk.Tk()
    root.title("EvB 5.1 v5 emulator")
    Evb(root).mainloop()

if __name__ == "__main__":
    main() 