from picamera import PiCamera
import os

command = "fswebcam --no-banner -r"
resolution = "1280x720"

fname = "image1.jpg"
dirName = "images"
filePath = os.path.dirname(os.path.realpath(__file__))
dirPath = os.path.join(filePath, dirName)
savePath = os.path.join(dirPath, fname)

class rpiCamera:
    def __init__(self):
        if(not os.path.exists(dirPath)):
            os.mkdir(dirPath)	
        #self.camera = PiCamera()
        #self.camera.resolution = (1280, 720)
        #self.camera.contrast = 10

    def captureImage(self):
        s = "%s %s %s" % (command, resolution, savePath)
        os.system(s)
        #self.camera.capture(savePath)


if __name__ == '__main__':
    rpi_cam = rpiCamera()
    rpiCamera.captureImage(rpi_cam)
