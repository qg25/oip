from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (1280, 720)
camera.contrast = 10

camera.capture('images/image1.jpg')
