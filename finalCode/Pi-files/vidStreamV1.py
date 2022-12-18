
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
from picamera import PiCamera
import datetime

# Raspberry Pi camera module (requires picamera package from Miguel Grinberg)
from camera_pi import Camera

app = Flask(__name__)

# Global variables definition and initialization
global panServoAngle
global tiltServoAngle
panServoAngle = 90
tiltServoAngle = 90

# Servo pin numre
panPin = 27
tiltPin = 17


@app.route('/')
def index():
    #Video streaming home page
    templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle,
	  'knapPause'		: str(knapPause)
	}
    return render_template('index.html', **templateData)


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
		#Legacy efter noget test


# genbrugt funktion til at starte/stoppe vid-stream
# nu brugt til at start streamen igen ved at linke tilbage til index med vid-streamen
@app.route("/start")
def startKnap():
    print("redirecting to stream site")
    templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle,
	}
    return render_template('index.html', **templateData)


# 'stopper' videostreamen ved at sende til en anden html side
@app.route("/stop")
def stopKnap():
    print("sending to picture site")
    templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle,
	}
    return render_template('picture.html', **templateData)


#Funktion der tager et billede med en cmd / shell command
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
	}
	return render_template('picture.html', **templateData, date = date)


#Generer 'billedet' til videostreamen i html
@app.route('/video_feed')
def video_feed():
	"""Video streaming route. 
	Put this in the src attribute of an img tag."""
	return Response(gen(Camera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')


#funktion lavet af MJrobot/Grinberg til at dreje servomotorer via html/flask
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
	}
	return render_template('index.html', **templateData)


# start flask på port 80
if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)
