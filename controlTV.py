##############################################################
#Name: controlTv.py
#Author: Konstantin Lausecker
#Date: 30.10.2020
#Description: This module is designed to control a tv for 24/7
#	      usage. The TV should display a website 24/7.
#             To save energy and ressources the tv should be
#             turned off if no motion was detected by using a
#             simple motion detector. 
#Version: 1.0
#Edits: None
#Needed dependencies: Os needs to install cec-utils
##############################################################
import os
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

noMotionDetectedTime = 60*5 #Time the Tv will stay on while no motion is detected in s

isSleeping = False
lastMotionDetected = datetime.now()


def turnOn():
        try:
                os.system("echo 'on 0' | cec-client -s -d 1")
                return True
        except Excpetion as e:
                println("An Exception occured: " + str(e))
                return False


def wakeUp(pin):
	global lastMotionDetected
	global isSleeping
	if(isSleeping):
		if(turnOn()):
			#print("AAAHAHAHH WAKEUP!!!")
			isSleeping = False
			lastMotionDetected = datetime.now()
		else:
			isSleeping = True
	else:
		#update Last motion time
		#print("Motion detected. Resetting timer")
		lastMotionDetected = datetime.now()
		isSleeping = False

def initGpio():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	motionPin = 7
	#Motiondetector input
	GPIO.setup(motionPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(motionPin, GPIO.RISING)
	GPIO.add_event_callback(motionPin, wakeUp)
def turnOff():
        try:
                os.system("echo 'standby 0' | cec-client -s -d 1")
                return True
        except Excpetion as e:
                println("An Exception occured: " + str(e))
                return False

def checkToSleep(isSleeping):
	global lastMotionDetected
	#check if it is time to sleep or not
	if(datetime.now() > (lastMotionDetected + timedelta(0,noMotionDetectedTime))):
		if(isSleeping == False):
			#print("I would turn off now")
			turnOff()
			return True
		else:
			#print("I am already asleep")
			return True
	else:
		time.sleep(0.1)
		#print("I think its no time to sleep, pepe")
	return False

if __name__ == "__main__":
	try:
		initGpio()
		while(True):
			isSleeping = checkToSleep(isSleeping)
			time.sleep(1)
	except KeyboardInterrupt as K:
		print(str(K))
