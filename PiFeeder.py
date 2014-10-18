#!/usr/bin/env python
# coding:utf-8 # weird bit error occuring from the pull from git. This was the fix
#
# PiFeeder.py  is an...
#
# Automated Cat Feeder using a Raspberry Pi and a servo
# Provides functionality for a button along with output buzzer
# to announce when it is time for the cat to eat. Provides a feedback
# loop for determining how much food to dole out.
# 
#

from RPIO import PWM     # PWM is the pulse width modulation library for a servo
import time              # To tell time… duh…
import RPi.GPIO as GPIO  # We need a way to send out and receive info lets use GPIO
import sys               # To close if the human makes an error


class Servo():
  def __init__(self,servo_pin,button_pin,beeper_pin):
  #Set up the GPIO pins before we initialize them
    self.ServoPin  = servo_pin  #18
    self.ButtonPin = button_pin #22
    self.BeeperPin = beeper_pin #24

#Initialize each pin and set GPIO mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.ButtonPin,GPIO.IN)
    GPIO.setup(self.BeeperPin,GPIO.OUT)
    GPIO.setup(self.PhotoPin1,GPIO.IN)
    GPIO.setup(self.PhotoPin2,GPIO.IN)

#make sure beeper is off
    GPIO.output(self.BeeperPin,False)
  #init our servo
    self.servo = PWM.Servo()
  #Size portions for servo sleeps
    self.FullServing = .75

    self.beepBoop(.2)
    self.beepBoop(.2)

  def button_pressed(self):
    return GPIO.input(self.ButtonPin)
 '''
 serv_CounterClockwise rotates a servo 
   in a CounterClockwise fashion. Cats 
   prefer to be fed from a Counterclockwise 
   rotating device and our servo is 
   mounted backwards 
   so we use this only to unstick
   stuck bits of tasty food
 '''
  def serv_CounterClockwise(self,ServoPIN,SleepTime):
  # Set servo on Servo1Pin to 2000s (2.0ms)
  # rotates ccw 
    self.servo.set_servo(ServoPIN, 2000)
    time.sleep(SleepTime)
    self.servo.stop_servo(ServoPIN)
    time.sleep(.25)

 '''
 serv_Clockwise rotates a servo in a 
   Clockwise fashion.  Studies
   from a major University(remains unnamed)
   show that cats prefer to be fed from a 
   Counter clockwise rotating device. 
   Since our servo is mounted backwards, 
   we will use this function to cater to our 
   overlords will.
 '''
  def serv_Clockwise(self,ServoPIN, SleepTime):
  # Set servo on ServoPin to 1200us (1.2ms)
  # This rotates the servo CW.
    self.servo.set_servo(ServoPIN, 1200)
    time.sleep(SleepTime)
    self.servo.stop_servo(ServoPIN)
    time.sleep(.25)


'''
 beepBoop beeps the hooper er … beeper
   announcing that our master of the 
   houses food is ready for his consumption
'''
  def beepBoop(self,sleepTime):
    GPIO.output(self.BeeperPin, True)
    time.sleep(sleepTime)
    GPIO.output(self.BeeperPin,False)
    time.sleep(sleepTime)

  '''
  feed_cat analyzes the bowl to see how much
    if any food remains in the bowl and then
    dishes out the correct portion of food.
    Humans always get it wrong so this will
    ensure the Cats are happy.
  '''
  def feed_cat(self):
  #feed the cat
    self.beepBoop(.15)
    time.sleep(.5)
    self.serv_Clockwise(self.ServoPin,self.FullServing)
    time.sleep(.5)
    self.serv_CounterClockwise(self.ServoPin,.05)
    

class PiFeeder():
  def __init__(self):
    self.servo1 = Servo(18,22,24)

  def feed_time(self,time1,time2):
    if time.strftime("%H") == time1[0] and time.strftime("%M") == time1[1]:
      self.servo1.feed_cat()
      catFed = True
      time.sleep(61)#there is a better way
    if time.strftime("%H") == time2[0] and time.strftime("%M") == time2[1]:
      self.servo1.feed_cat()
      catFed = True
      time.sleep(61)#there is a better way

  def button1_pushed(self):
    return self.servo1.button_pressed()

  def force_feed(self, servo):
    if servo == 1:
      self.servo1.feed_cat()


# Ask the user if the time was set. This needs to be done
# on a raspberry because the internal clock gets cooky
# when off power for a short period of time


def get_Time(num):
    invalidTime = True
    while (invalidTime):
      time = raw_input("Please enter time " + num + " seperating hour and minute by spaces (i.e 22 30)").split()
      if int(time[0]) > 23:
        print "invalid hour"
      elif int(time[1]) > 59:
        print "invalid minute"
      else:
        invalidTime = False
    return time

def main():
  
  feeder = PiFeeder()

  feedTimes = raw_input("Would you like to set times to feed the cat?(y/n)")
  feedAtTimes = False

  if feedTimes.lower() == "y":
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
        print "This can be done with date —set i.e."
        print "sudo date --set=(quote)9 AUG 2013 16:15:00(quote) "
        sys.exit()
      else:
        timeSet = raw_input("I'm sorry, I didn't get that. Try again (y/n)")

    feedAtTimes = True
  # setting when our masters want to be fed.

    feed_time_1 = get_Time("1")
    feed_time_2 = get_Time("2")
    print ("Feeding times are " + feed_time_1[0] + ":" + feed_time_1[1] + " and " + feed_time_2[0] + ":" + feed_time_2[1] + ".")

  #Everythings all set! lets get running!
  print "Thank you, PiFeeder is now running"

  # loop … forever … theres no way out of this
  while True:
    if(feeder.button1_pushed()):
      print "Button Pressed"
      feeder.force_feed()
    feeder.feed_time(feed_time_1, feed_time_2)
    



if __name__ == "__main__": 
  main()

  
