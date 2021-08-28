from picamera import PiCamera
import os

fname = "image1.jpg"
dirName = "images"
filePath = os.path.dirname(os.path.realpath(__file__))
dirPath = os.path.join(filePath, dirName)
savePath = os.path.join(dirPath, fname)

class rpiCam:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.contrast = 10

    def captureImage(self):
        self.camera.capture(savePath)


if __name__ == '__main__':
    rpi_cam = rpiCam()
    rpiCam(rpi_cam).captureImage()