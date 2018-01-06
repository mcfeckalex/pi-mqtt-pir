import RPi.GPIO as GPIO
import time
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from subprocess import call
from subprocess import check_output

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
   print list
   if filename in list:
      return True
   else:
      return False

off_sent = False
input_state = False
#pir loop:-
while True:   
   print "start wait.."
   while input_state == False:
      input_state = GPIO.input(18)
   input_state = False
   curr_date = time.strftime('%y-%m-%d')
   time_now = time.strftime('%y-%m-%d-%H%M%S')
   db_snap_path = db_cam_path+cam_location+curr_date
   snap_filename = db_snap_path+"/"+time_now+".jpeg"
   publish.single(state_topic, 'on', hostname=broker)
   call(["wget", "http://raspberrypi:8080/stream/snapshot.jpeg?delay_s=3", "-O", time_now+".jpeg"])
   if db_if_exists(curr_date):
      call([uploader_path, "upload", script_path+time_now+".jpeg", snap_filename])
   else:
      call([uploader_path, "mkdir", db_snap_path])
      call([uploader_path, "upload", script_path+time_now+".jpeg", snap_filename])
   
   dir_name = "/home/pi/mqtt/mqtt-pir/"
   test = os.listdir(dir_name)

   for item in test:
      if item.endswith(".jpeg"):
         os.remove(os.path.join(dir_name, item))
   time.sleep(delay)
   
   publish.single(state_topic, 'off', hostname=broker)