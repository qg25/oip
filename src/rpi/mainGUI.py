#!/usr/bin/env python3

from guizero import App, PushButton, info, Window, Text
from functools import partial
# from gpiozero import LED
import sys
from rpiToArduino import rpi2Arduino
import threading
import concurrent.futures

# led = LED(21)
jobs = ["Cleaning", "Drying"]
CLEANING = 1
DRYING = 2

def exitApplication():
    if app.yesno("Quit...", "Do you want to quit?"):
        app.destroy()
        sys.exit()

def beginProgram(jobType):
    # led.toogle()
    # if led.is_lit:
    #     ledButton.text = "Drying started"
    print("job: ", jobType)
    # else:
    #     ledButton.text = "Start Drying"
    # app.info("Info", jobs[jobType-1] + " process started!!!")
    # text.value = jobs[jobType-1] + " process started!!!"
    # t = threading.Thread(target=displayMsg, args=(jobType,))
    # t.start()
    """

    t = threading.Thread(target=comms.communications, args=(jobType,))
    t.start()
    # t.join()
    # window.hide()
    app.info("Info", jobs[jobType-1] + " process finished!!!")

    # if comms.communications(jobType):
    #     app.info("Info", jobs[jobType-1] + " process finished!!!")
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(comms.communications, jobType)
        return_value = future.result()
        print(return_value)
        if return_value:
            # window.hide()
            app.info("Info", jobs[jobType-1] + " process finished!!!")
            pass

def displayMsg(jobType):
    text.value = jobs[jobType-1] + " process started!!!"
    window.show()


if __name__ == '__main__':
    app = App("Gui", height=480, width=800)
    window = Window(app, title = "", height=240, width=400)
    text = Text(window, text="hi", align="left", width="fill")
    window.hide()

    comms = rpi2Arduino()

    cleaningButton = PushButton(app, partial(beginProgram, CLEANING), text="Start Cleaning", align="top", width=15, height=2)
    cleaningButton.text_size = 30

    dryingButton = PushButton(app, partial(beginProgram, DRYING), text="Start Drying", width=15, height=2)
    dryingButton.text_size = 30

    exitButton = PushButton(app, exitApplication, text="Exit", align="bottom", width=15, height=2)
    exitButton.text_size = 30
    exitButton.text_color = "red"

    app.display()