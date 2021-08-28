import serial
import time
import platform
import sys
from checkConditions import checkCondition

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

        #self.ser.setDTR(False)
        #time.sleep(1)
        #self.ser.flushInput()
        #self.ser.setDTR(True)
        #time.sleep(2)
    def exitProgram(self, exiting):
        self.ser.write(str(exiting).encode('utf-8'))
        

    def communications(self, jobType):
        global isDirty
        global isWet
        isWet = True
        isDirty = True

        while True:
            if jobType == EXIT:
                self.sendJob(EXIT)
                break
            
            if jobType == FULL_CYCLE and isDirty:
                self.sendJob(WASHING)
                isDirty = checkCondition.checkCleanliness(self.checks)
            elif (jobType == FULL_CYCLE or jobType == HALF_CYCLE) and isWet:
                self.sendJob(DRYING)
                isWet = checkCondition.checkDryness(self.checks)
            else:
                self.sendJob(STERILIZING)
                break
        return True
    

    def sendJob(self, jobType):
        self.ser.write(str(jobType).encode('utf-8'))
        while True:
            if self.ser.in_waiting > 0:
                #print('\nreceive')
                self.line = self.ser.readline().decode('utf-8').rstrip()
                print(self.line)
                if self.line == JobDone:
                    self.line = ""
                    break
                print(self.line)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        comms = rpi2Arduino()
        rpi2Arduino.communications(comms, sys.argv[1])
