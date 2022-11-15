
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCamPanTilt.py
#  	Streaming video with Flask based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with PanTilt position Control
#
#   MJRoBot.org 30Jan18

import os
import subprocess
from time import sleep
from flask import Flask, render_template, request, Response
#det vi bruger til at tage billeder/knap
#from picamera.array import PiRGBArray
#import time
from picamera import PiCamera
import datetime
#from signal import pause
#from gpiozero import Button
#import pigpio
# Raspberry Pi camera module (requires picamera package from Miguel Grinberg)
from camera_pi import Camera

app = Flask(__name__)

# Global variables definition and initialization
global panServoAngle
global tiltServoAngle
panServoAngle = 90
tiltServoAngle = 90
global knapPause
knapPause = False
#knap
#button = Button(4)
# Servo pin numre
panPin = 27
tiltPin = 17
#camera til at tage billeder:
#cam = PiCamera()
#cam.resolution = (1920, 1080)
#cam.vflip = True
#cam.contrast = 10
#cam.framerate = 32


@app.route('/')
def index():
    #Video streaming home page
    templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle,
	  'knapPause'		: str(knapPause)
	}
    return render_template('index.html', **templateData)


#function til at tage billede flyttet til camera_pi som static method
#def picture():
#	date = str(datetime.datetime.now())
#	file_name = f'/home/g4py/kamera/billeder/pic_{date}.png'
#	cam.capture(file_name)
#	print("pic taken")


# Inkorperer en knap der tænder og slukker for video stream funktionen
#flyttet til en anden html side i stedet for tænd/sluk
def gen(camera):
	#Video streaming generator function.
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
	else:
		print("Test råb")

# Knap funktion der tænder og slukker for video streamen
# den kommer til at linke til en anden html side der streames til
@app.route("/start")
def startKnap():
#	global knapPause
#	global panServoAngle
#	global tiltServoAngle
#
#	if 'startstop':
#		if knapPause == True:
#			knapPause = False
#		else:
#			knapPause = True
    print("redirecting to stream site")
    return render_template('index.html')


# vi skal finde en måde at de-init kamera streamen
@app.route("/stop")
def stopKnap():
    print("sending to picture site")
    templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle,
	  'knapPause'		: str(knapPause)
	}
    return render_template('picture.html', **templateData)


@app.route('/snap')
def snapPic():
	sleep(1)
	rawDate = str(datetime.datetime.now())
	rawDate = rawDate[:19]
	date = rawDate.replace(" ", "_")
	cmd = f'raspistill --width 1080, --height 640 -vf -o /home/g4py/code/billeder/pic_{date}.png'
	print(cmd)
	subprocess.call(cmd, shell=True)
	sleep(0.5)
	print("Camera.picture has been called")
	
	templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle,
	  'knapPause'		: str(knapPause)
	}
	return render_template('picture.html', **templateData, date = date)


@app.route('/video_feed')
def video_feed():
	"""Video streaming route. 
	Put this in the src attribute of an img tag."""
	return Response(gen(Camera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route("/<servo>/<angle>")
def move(servo, angle):
	global panServoAngle
	global tiltServoAngle
	if servo == 'pan':
		if angle == '+':
			panServoAngle = panServoAngle + 10
		else:
			panServoAngle = panServoAngle - 10
		os.system("python3 angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
	if servo == 'tilt':
		if angle == '+':
			tiltServoAngle = tiltServoAngle + 10
		else:
			tiltServoAngle = tiltServoAngle - 10
		os.system("python3 angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))

	templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle,
	  'knapPause'		: str(knapPause)
	}
	return render_template('index.html', **templateData)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)
