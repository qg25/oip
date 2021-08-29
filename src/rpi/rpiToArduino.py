import serial
import time
import platform
import sys
import threading
from checkConditions import checkCondition
from telegrambot.telebot import teleNotification
from rpiCam import rpiCamera
fname = ["dirty.jpg", "clean.jpg"]
fname2 = ["wet.jpg", "dry.jpg"]


jobs = ["Full-Cycle", "Half-Cycle"]
FULL_CYCLE = 0
HALF_CYCLE = 1
WASHING = 1
DRYING = 2
STERILIZING = 3
EXIT = 4
JobDone = '1'


class rpi2Arduino:
    def __init__(self):
        currentSys = platform.system()
        if (currentSys == "Windows"):
            self.ser = serial.Serial(port='COM4', baudrate=9600, timeout=1)
        else:
            self.ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
        self.ser.flush()

        print('Program Start')
        self.line = ""

        self.checks = checkCondition()
        self.camera = rpiCamera()
        
        self.t = threading.Thread(target=teleNotification)
        self.t.start()


    def exitProgram(self):
        self.ser.write(str(EXIT).encode('utf-8'))
        teleNotification.stopTelebot(self.t)


    def communications(self, jobType):
        global isClean
        global isDry
        isClean = False
        isDry = False
        count = 0
        counts = 0

        while True:
            print("clean?: ", isClean)
            
            if jobType == FULL_CYCLE and not isClean:
                self.sendJob(WASHING)
                rpiCamera.captureImage(self.camera, WASHING)
                isClean = checkCondition.checkCleanliness(self.checks, fname[counts])
                counts=1
                print("after?: ", isClean)
            elif not isDry:
                self.sendJob(DRYING)
                rpiCamera.captureImage(self.camera, DRYING)
                isDry = checkCondition.checkDryness(self.checks, fname2[count])
                count=1
            else:
                self.sendJob(STERILIZING)
                break
                
        teleNotification.sendNotification(self.t, jobs[jobType])
        rpiCamera.closeCamera(self.camera)
        return True
    
    
    def sendJob(self, jobType):
        self.ser.write(str(jobType).encode('utf-8'))
        while True:
            if self.ser.in_waiting > 0:
                self.line = self.ser.readline().decode('utf-8').rstrip()
                print(self.line)
                if self.line == JobDone:
                    self.line = ""
                    break
                print(self.line)
                
                
    def stopThread(self):
        self.t.join()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        comms = rpi2Arduino()
        rpi2Arduino.communications(comms, sys.argv[1])
