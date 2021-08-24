import os
import sys
import platform

def create(currentSys):
    global command

    if (currentSys == "Windows"):
        command = "python -m venv env"
    elif (currentSys == "Darwin"):
        os.system("virtualenv env")
        command = "virtualenv env --system-site-packages"
    else:
        command = "python3 -m venv env"

def clean(currentSys):
    global command

    if (currentSys == "Windows"):
        command = "rmdir /S /Q src\\rpi\__pycache__ env"
    else:
        command = "rm -rf src/rpi/__pycache__"


if ( __name__ == "__main__"):
    currentSys = platform.system()
    if (sys.argv[1] == "create"):
        create(currentSys)
    elif (sys.argv[1] == "clean"):
        clean(currentSys)
    else:
        print("Invalid args")
        
    print(command)
    os.system(command)
