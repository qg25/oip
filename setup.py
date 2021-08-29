import os
import sys
import shutil
import platform

def create(currentSys):
    global command

    if (currentSys == "Windows"):
        command = "python -m venv env"
    else:
        command = "python3 -m venv env"


def clean(currentSys):
    global command

    if (currentSys == "Windows"):
        command = "rmdir /S /Q env"
        clearCache()
    else:
        command = "rm -rf env"
        clearCache()


def clearCache():
    path = os.path.dirname(os.path.realpath(__file__))
    srcDirPath = os.path.join(path, "src")
    cachePath = os.path.join(srcDirPath, "rpi")
    print(cachePath)
    for directories, subfolder, files in os.walk(cachePath):
        if os.path.isdir(directories):
            if directories[::-1][:11][::-1] == '__pycache__':
                            shutil.rmtree(directories)


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
