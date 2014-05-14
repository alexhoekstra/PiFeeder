#!/usr/bin/env python
#
# PiFeeder.py  is an...
#
# Automated Cat Feeder using a Raspberry Pi and a servo
# Provides functionality for a button along with output buzzer
# to announce when it is time for the cat to eat. Provides a feedback
# loop for determining how much food to dole out.
# 
# Hardware help came from http://drstrangelove.net/2013/12/raspberry-pi-power-cat-feeder-updates/
# David Bryan’s Blog
# (IE help with how to set servo clockwise and counter clockwise and with a basic breadboard layout)
#

from RPIO import PWM     # PWM is the pulse width modulation library for a servo
import time              # To tell time… duh…
import RPi.GPIO as GPIO  # We need a way to send out and receive info lets use GPIO
import sys               # To close if the human makes an error


#Set up the GPIO pins before we initialize them
ServoPin=18
ButtonPin=22
BeeperPin=24
PhotoPin1=17
PhotoPin2=21

#Initialize each pin and set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(ButtonPin,GPIO.IN)
GPIO.setup(BeeperPin,GPIO.OUT)
GPIO.setup(PhotoPin1,GPIO.IN)
GPIO.setup(PhotoPin2,GPIO.IN)

#make sure beeper is off
GPIO.output(BeeperPin,False)


servo = PWM.Servo()

###########################################
# serv_CounterClockwise rotates a servo 
#   in a CounterClockwise fashion. Studies
#   from a major University(remains unnamed)
#   show that cats prefer to be fed from a 
#   clockwise rotating device. Since our 
#   servo is mounted backwards, we will use 
#   this function to cater to our 
#   overlords will.
############################################
def serv_CounterClockwise(ServoPIN,SleepTime):
  # Set servo on Servo1Pin to 2000s (2.0ms)
  # rotates ccw 
  # thanks to David Bryan
  servo.set_servo(ServoPIN, 2000)
  time.sleep(SleepTime)
  servo.stop_servo(ServoPIN)
  time.sleep(.25)



###########################################
# serv_Clockwise rotates a servo in a 
#   Clockwise fashion. Cats prefer to be
#   fed from a clockwise rotating device
#   and our servo is mounted backwards 
#   so we use this only to unstick
#   stuck bits of tasty food
############################################
def serv_Clockwise(ServoPIN, SleepTime):
  # Set servo on ServoPin to 1200us (1.2ms)
  # This rotates the servo CW.
  # thanks to David Bryan
  servo.set_servo(ServoPIN, 1200)
  time.sleep(SleepTime)
  servo.stop_servo(ServoPIN)
  time.sleep(.25)


#############################################
# beepBoop beeps the hooper er … beeper
#   announcing that our master of the 
#   houses food is ready for his consumption
#############################################
def beepBoop(sleepTime):
  GPIO.output(BeeperPin, True)
  time.sleep(sleepTime)
  GPIO.output(BeeperPin,False)


#############################################
# feedCat analyzes the bowl to see how much
#   if any food remains in the bowl and then
#   dishes out the correct portion of food.
#   Humans always get it wrong so this will
#   ensure the Cats are happy.
#############################################
def feedCat():
  #feed the cat
  if (GPIO.input(PhotoPin1) == True):#if empty
    beepBoop(.15)
    print "bowl empty"
    time.sleep(.5)
    serv_Clockwise(ServoPin,2)
    time.sleep(.5)
    serv_CounterClockwise(ServoPin,.1)
  elif (GPIO.input(PhotoPin2) == True):#if not empty but not full
    beepBoop(.15)
    print "bowl not empty"
    time.sleep(.5)
    serv_Clockwise(ServoPin,1.5)
    time.sleep(.5)
    serv_CounterClockwise(ServoPin,.05)
  else: #assume empty
    beepBoop(.15)
    print "assumed bowl empty"
    time.sleep(.5)
    serv_Clockwise(ServoPin,2)
    time.sleep(.5)
    serv_CounterClockwise(ServoPin,.05)
    
###############################################  
# validHour(num) receives a number which will
#   then prompt the user with the grammatically
#   correct version for when our overlords would
#   like to be fed. It checks that number to
#   see if it exists within the 24 hour clock
#   and if it does, returns it, if not, prompts
#   the user for a valid hour
###############################################    
def validHour(num):
  notSet = True
  feedHour = input("What is the " + feedTime(num) + " hour you would like to feed him at? (24 hr format)")
  while notSet:  
    if (feedHour >= 0 and feedHour <= 24):
      notSet = False
    else:
      feedHour = input("I'm sorry, thats an invalid hour, please try again")
  return feedHour      

###############################################  
# validMinute(num) receives a number which will
#   then prompt the user with the grammatically
#   correct version for when our overlords would
#   like to be fed. It checks that number to
#   see if it exists within the 60 minute clock
#   and if it does, returns it, if not, prompts
#   the user for a valid minute
###############################################  
def validMinute(num):
  notSet = True
  feedMinute = input("What is the " + feedTime(num) +" minute would like to feed him at? (60 min format)")
  while notSet:  
    if (feedMinute >= 0 and feedMinute <= 60):
      notSet = False
    else:
      feedMinute = input("I'm sorry, thats an invalid Minute, please try again")
  return feedMinute 

###############################################  
# feedTime(num) receives a number and assumes
#  if its not 1 then it must be 2 (cats don’t
#  eat more than twice silly human) and returns
#  the grammatically correct version of that 
#  number
###############################################  
def feedTime(num):
  if num == 1:
    return "first"
  else:
    return "second"



# Ask the user if the time was set. This needs to be done
# on a raspberry because the internal clock gets cooky
# when off power for a short period of time

timeSet = raw_input("Have you remembered to set the clock? (y/n)") 

noTimeSet = True

# if the user set the time.. were all cool,
# if they didn’t, we tell him what’s what and exit the program
# if they enter a weird value in… humans do that sometimes,
# then we ask them again

while noTimeSet:
  if timeSet.lower() == "y":
    noTimeSet = False
  elif timeSet.lower() == "n":
    print "Please set the time and run the program again"
    print “This can be done with date —set i.e.”
    print “sudo date --set=(quote)9 AUG 2013 16:15:00(quote) ”
    sys.exit()
  else:
    timeSet = raw_input("I'm sorry, I didn't get that. Try again (y/n)")

# setting when our masters want to be fed.
feedHour1 = validHour(1)
feedMinute1 = validMinute(1)
feedHour2 = validHour(2)
feedMinute2 = validMinute(2)

print "Thank you, Pifeeder is now running”
print ("Feeding times are " + feedHour1 + ":" + feedMinute1 + " and " + feedHour2 + ":" + feedMinute2 + ".")


catFed = False # switch to see whether we fed the cat this minute or not
               # this is done so we can use the button if our cat requires
               # more food than was put out... some cats are pretty fat...

# loop … forever … theres no way out of this
while True:
  if(GPIO.input(ButtonPin) == True):
    feedCat()
  if time.strftime("%H") == str(feedHour1) and time.strftime("%M") == str(feedMinute1) and catFed == False:
    feedCat()
    catFed = True
  if time.strftime("%H") == str(feedHour2) and time.strftime("%M") == str(feedMinute2) and catFed == False:
    feedCat()
    catFed = True
  if ((time.strftime(“%M”) == str(feedMinute1 + 1) or time.strftime(“%M”) == str(feedMinute2 +1)) and catFed == True):
      catFed = False #reset the switch... its been a minute
  

  
