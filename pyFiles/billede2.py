#!/usr/bin/python
from picamera.array import PiRGBArray
import pigpio
import time
from gpiozero import Button
from signal import pause
from picamera import PiCamera
import datetime
#KNAP_GPI_PIN = 4
button = Button(4)


#knap = pi.read(KNAP_GPI_PIN)
level = 0
dir = 1
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.vflip = True
camera.contrast = 10
camera.framerate = 32
#camera.image_effect = "watercolor"
#file_name = "/home/g4py/SFTP/testmappe2/img_" + str(datetime.datetime.now()) + ".png"
"""rawCapture = PiRGBArray(camera, size=(640, 480))"""

def picture():
	date = str(datetime.datetime.now())
	file_name = f'/home/g4py/SFTP/testmappe3/pic_{date}.png'
	camera.capture(file_name)
	print("Pic taken")

while True:
	try:
		if button.is_pressed:
			picture()
			#camera = PiCamera()
			#camera.capture(file_name)
			time.sleep(0.5)
			#print("Done.")
			level += dir
			#camera.close()
			print("Done.")
		#elif button.is_released:
		#	print("rigtigt done")
	except KeyboardInterrupt:
		print("ctrl+c exit")
		quit()

