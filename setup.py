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


if ( __name__ == "__main__"):
    currentSys = platform.system()
    if (sys.argv[1] == "create"):
        create(currentSys)

    print(command)
    os.system(command)