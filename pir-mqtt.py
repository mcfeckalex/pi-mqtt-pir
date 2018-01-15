import RPi.GPIO as GPIO
import time
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from subprocess import call
from subprocess import check_output
import logging
#logging setup
LOG_LEVEL = logging.DEBUG
LOG_FILE = "/home/pi/mqtt/mqtt-pir/pir_mqtt.log"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.IN)

cam_location = "hallen/"

snapshot_command = "http://raspberrypi:8080/stream/snapshot.jpeg?delay_s=0"

uploader_path =  "/home/pi/Dropbox-Uploader/dropbox_uploader.sh"
db_cam_path = "/pi_cam/"
script_path = os.path.dirname(os.path.realpath(__file__))+"/"

broker = '192.168.1.80'
state_topic = 'home-assistant/pir/state'
delay=1

def db_if_exists(filename, path = db_cam_path+cam_location):
   print uploader_path
   list = check_output([uploader_path, "list", path])
   if filename in list:
      return True
   else:
      return False

off_sent = False
input_state = False
#pir loop:-
while True:   
   logging.debug("Waiting for motion...")

   while input_state == False:
      input_state = GPIO.input(18)
   input_state = False
   logging.debug("motion detected...")
   curr_date = time.strftime('%y-%m-%d')
   time_now = time.strftime('%y-%m-%d-%H%M%S')
   db_snap_path = db_cam_path+cam_location+curr_date
   snap_filename = db_snap_path+"/"+time_now+".jpeg"
   publish.single(state_topic, 'on', hostname=broker)
   logging.debug("downloading snapshot..." )
   call(["wget", "http://raspberrypi:8080/stream/snapshot.jpeg?delay_s=3", "-O", script_path+time_now+".jpeg"])
   if db_if_exists(curr_date):
      call([uploader_path, "upload", script_path+time_now+".jpeg", snap_filename])
   else:
      call([uploader_path, "mkdir", db_snap_path])
      call([uploader_path, "upload", script_path+time_now+".jpeg", snap_filename])
   
   
   test = os.listdir(script_path)
   logging.debug("Files in script dir:\n"+str(test))
   for item in test:
      if item.endswith(".jpeg"):
         logging.debug("removing snapshot "+os.path.join(script_path, item))
         os.remove(os.path.join(script_path, item))
   time.sleep(delay)

   publish.single(state_topic, 'off', hostname=broker)
