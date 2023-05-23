##############################################################
#Name: controlTv.py
#Author: Konstantin Lausecker
#Date: 30.10.2020
#Modified: 23.05.2023
#Description: This module is designed to control a tv for 24/7
#	      		usage. The TV should display a website 24/7.
#             	To save energy and ressources the tv should be
#             	turned off if no motion was detected by using a
#             	simple motion detector. 
#Version: 1.1
#Edits: -V1.1: Added comments and cleanup
#Needed dependencies: Os needs to install cec-utils
##############################################################
import os
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

# User defined variables
noMotionDetectedTime = 60*5 #Time the Tv will stay on while no motion is detected in s
motionPin = 7				 #Pin which is used for motion detector --> Change

# Global variables
isSleeping = False
lastMotionDetected = datetime.now()

# Function to turn on the tv
def turnOn():
	try:
		os.system("echo 'on 0' | cec-client -s -d 1")
		return True
	except Excpetion as e:
		println("An Exception occured: " + str(e))
		return False

# Function to turn off the tv
def turnOff():
	try:
		os.system("echo 'standby 0' | cec-client -s -d 1")
		return True
	except Excpetion as e:
		println("An Exception occured: " + str(e))
		return False

# Interrupt function to wake up --> Triggered by motion detector
# pin: Pin which triggered the interrupt (not used haha)
def wakeUp(pin):
	global lastMotionDetected	 # Get global var lastMotionDetected
	global isSleeping			 # Get global var isSleeping

	if(isSleeping): # If tv is sleeping, wake it up
		if(turnOn()):
			#print("AAAHAHAHH WAKEUP!!!")
			isSleeping = False
			lastMotionDetected = datetime.now() # Reset timer
		else:
			isSleeping = True

	else:			 # If tv is already awake, reset timer
		#print("Motion detected. Resetting timer")
		lastMotionDetected = datetime.now() # Reset timer
		isSleeping = False

# Function to initialize the GPIOs
def initGpio():
	GPIO.setmode(GPIO.BOARD) 	# Use board pin numbering
	GPIO.setwarnings(False) 	# Disable warnings
	global motionPin			# Pin used for motion detector
	
	GPIO.setup(motionPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set motionPin as input with pull down resistor

	GPIO.add_event_detect(motionPin, GPIO.RISING) # Add interrupt to motionPin when voltage is rising
	GPIO.add_event_callback(motionPin, wakeUp)	 # Add callback function to motionPin -> wakeup(motionPin)

# Function to check if it is time to sleep
# isSleeping: Boolean which indicates if the tv is sleeping or not
# return: Boolean which indicates if it is time to sleep or not
def checkToSleep(isSleeping):
	global lastMotionDetected # Get global var lastMotionDetected

	#check if it is time to sleep or not
	if(datetime.now() > (lastMotionDetected + timedelta(0,noMotionDetectedTime))):
		if(isSleeping == False): # TV is awake
			turnOff()
			return True
		else: 					 # TV already sleeps
			#print("I am already asleep")
			return True
	else:
		time.sleep(0.1) # Wait 100ms
		#print("I think its no time to sleep, pepe")

	return False

# Main function to start the program when called directly
if __name__ == "__main__":
	try:
		initGpio() 	# Initialize GPIOs
		while(True): # Main loop
			isSleeping = checkToSleep(isSleeping) 	# Check if it is time to sleep
			time.sleep(1)					 		# Wait 1s
	except KeyboardInterrupt as K:
		print(str(K))
