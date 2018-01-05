import RPi.GPIO as GPIO
import time
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.IN)

broker = '192.168.1.80'
state_topic = 'home-assistant/pir/state'
delay=1

#pir loop:-
while True:
   time_now = time.strftime('%y-%m-%d-%H%M%S')
   input_state = GPIO.input(18)
   if input_state == True:
      publish.single(state_topic, 'on', hostname=broker)
   else:
      publish.single(state_topic, 'off', hostname=broker)
   time.sleep(delay)
