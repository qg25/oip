from typing import Text
from guizero import App, PushButton
from gpiozero import LED
import sys

led = LED(21)

def exitDry():
    sys.exit()

def startDry():
    led.toggle()
    if led.is_lit:
        ledButton.text = "Drying started"
    else:
        ledButton.text = "Start Drying"

    
if __name__ == '__main__':
    app = App("Gui", height = 480, width=800)

    ledButton= PushButton(app, startDry, text="Start Drying", align="top", width=15, height=4)
    ledButton.text_size=36

    exitButton= PushButton(app, exitDry, text="Exit", align="bottom", width=15, height=4)
    exitButton.text_size=36

    app.display()
    