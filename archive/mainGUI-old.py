#!/usr/bin/env python3

from guizero import App, PushButton, info, Window, Text
from functools import partial
from rpiToArduino import rpi2Arduino
import sys
import concurrent.futures
import threading
from telegrambot.telebot import teleNotification

jobs = ["Full-Cycle", "Half-Cycle"]
FULL_CYCLE = 0
HALF_CYCLE = 1
WIN_WIDTH=500
WIN_HEIGHT=380
TEXT_SIZE = 30
RED = "red"
threads = []


def exitApplication():
    if app.yesno("Quit...", "Do you want to quit?"):
        comms.exitProgram()
        app.destroy()
        sys.exit()

def beginProgram(jobType):
    displayMsg(jobType)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(comms.communications, jobType)
        return_value = future.result()
        print(return_value)
        if return_value:
            window.hide()
            app.info("Info", jobs[jobType] + " process finished!!!")


def displayMsg(jobType):
    global window
    window = Window(app, title = "Process", height=WIN_HEIGHT, width=WIN_WIDTH)
    
    text = Text(window, text=jobs[jobType] + " process started!!!\n\nPlease wait...", align="left", width="fill")
    text.text_size = TEXT_SIZE
    
    screen_width = app.tk.winfo_screenwidth()
    screen_height = app.tk.winfo_screenheight()
    x = (screen_width/2) - (WIN_WIDTH/2)
    y = (screen_height/2) - (WIN_HEIGHT/2)
    window.tk.geometry('%dx%d+%d+%d' % (WIN_WIDTH, WIN_HEIGHT, x, y))
    
    window.show()
    window.update()
   
   
if __name__ == '__main__':    
    app = App("Gui", height=480, width=800)
    #app.tk.attributes("-fullscreen", True)

    comms = rpi2Arduino()

    cleaningButton = PushButton(app, partial(beginProgram, FULL_CYCLE), text="Start Full-Cycle", align="top", width=15, height=2)
    cleaningButton.text_size = TEXT_SIZE

    dryingButton = PushButton(app, partial(beginProgram, HALF_CYCLE), text="Start Half-Cycle", width=15, height=2)
    dryingButton.text_size = TEXT_SIZE

    exitButton = PushButton(app, exitApplication, text="Exit", align="bottom", width=15, height=2)
    exitButton.text_size = TEXT_SIZE
    exitButton.text_color = RED
    
    print('Displaying...')
    app.display()
    
