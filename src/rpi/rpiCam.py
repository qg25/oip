from picamera import PiCamera
import time


class rpiCam:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.contrast = 10

    def captureImage(self):
        self.camera.capture('images/image1.jpg')


if __name__ == '__main__':
    rpi_cam = rpiCam()
    rpiCam(rpi_cam).captureImage()