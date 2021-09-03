import serial
import platform
import sys
import threading
from checkConditions import checkCondition
from telegrambot.telebot import teleNotification
from rpiCam import rpiCamera
import webbrowser

fname2 = ["wet.jpg", "dry.jpg"]

STAIN_CHECK = "SC"
DRY_CHECK = "DC"
DRY_CHECK2 = "DC2"

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
        
        url = "http://localhost:5000/"
        webbrowser.open(url)
        
        self.t = threading.Thread(target=teleNotification)
        self.t.start()


    def exitProgram(self):
        self.ser.write(str(EXIT).encode('utf-8'))
        rpiCamera.closeCamera(self.camera)
        teleNotification.stopTelebot(self.t)


    def communications(self, jobType):        
        print("Job: ", jobType)
        if jobType == WASHING:
            return self.sendJob(WASHING)
            
        if jobType == DRYING:
            return self.sendJob(DRYING)
            
        if jobType == STERILIZING:
            return self.sendJob(STERILIZING)
            
        if jobType == STAIN_CHECK:
            rpiCamera.captureImage(self.camera, WASHING)
            isClean = checkCondition.checkCleanliness(self.checks)
            return isClean

        if jobType == DRY_CHECK:
            rpiCamera.captureImage(self.camera, DRYING)
            isDry = checkCondition.checkDryness(self.checks, fname2[0])
            return isDry
            
        if jobType == DRY_CHECK2:
            rpiCamera.captureImage(self.camera, DRYING)
            isDry = checkCondition.checkDryness(self.checks, fname2[1])
            return isDry

        teleNotification.sendNotification(self.t, jobType)
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
        return True
                
                
    def stopThread(self):
        self.t.join()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        comms = rpi2Arduino()
        rpi2Arduino.communications(comms, sys.argv[1])
