from picamera import PiCamera
import os


fname = ["cleanImg.jpg", "dryImg.jpg"]
dirName = "images"
filePath = os.path.dirname(os.path.realpath(__file__))
dirPath = os.path.join(filePath, dirName)


class rpiCamera:
    def __init__(self):
        if(not os.path.exists(dirPath)):
            os.mkdir(dirPath)	
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.contrast = 10

    def captureImage(self, imgType):
        savePath = os.path.join(dirPath, fname[imgType-1])
        self.camera.capture(savePath)
            
    def closeCamera(self):
        self.camera.close()

if __name__ == '__main__':
    rpi_cam = rpiCamera()
    rpiCamera.captureImage(rpi_cam,1)
