import serial
import time
import platform
import sys

WASHING = 1
DRYING = 2
isWet = True
isDirty = True
JobDone = '1'


class rpi2Arduino:
    def __init__(self):
        currentSys = platform.system()
        if (currentSys == "Windows"):
            self.ser = serial.Serial(port='COM4', baudrate=9600, timeout=1)
        else:
            self.ser = serial.Serial(port='/dev/ttyACM1', baudrate=9600, timeout=1)
        self.ser.flush()

        print('Program Start')
        self.line = ""

        #self.ser.setDTR(False)
        #time.sleep(1)
        #self.ser.flushInput()
        #self.ser.setDTR(True)
        #time.sleep(2)
        

    def communications(self, jobType):
        self.ser.write(str(jobType).encode('utf-8'))
        while (True):
            if self.ser.in_waiting > 0:
                #print('\nreceive')
                self.line = self.ser.readline().decode('utf-8').rstrip()
                print(self.line)
                if self.line == JobDone:
                    self.line = ""
                    break
                print(self.line)
        return True


if __name__ == '__main__':
    if len(sys.argv) > 1:
        comms = rpi2Arduino()
        rpi2Arduino.communications(comms, sys.argv[1])
