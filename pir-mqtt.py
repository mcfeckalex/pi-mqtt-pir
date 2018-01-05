import RPi.GPIO as GPIO
import time
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.IN)


snapshot_command = "http://raspberrypi:8080/stream/snapshot.jpeg?delay_s=0"

uploader_path =  "../Dropbox-Uploader/dropbox_uploader.sh"
db_cam_path = "/pi_cam/cam_1"
script_path = os.path.dirname(os.path.realpath(__file__))


broker = '192.168.1.80'
state_topic = 'home-assistant/pir/state'
delay=3

def db_if_exists(filename):
   list = check_output([uploader_path, "list", "pi_cam/cam_1"])
   print list
   if filename in list:
      return True
   else:
      return False

#pir loop:-
while True:
   time_now = time.strftime('%y-%m-%d-%H%M%S')
   input_state = GPIO.input(18)
   if input_state == True:
      publish.single(state_topic, 'on', hostname=broker)
   else:
      publish.single(state_topic, 'off', hostname=broker)
   time.sleep(delay)
