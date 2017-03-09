import os
import time
from pprint import pprint

import _thread
import camera_rpi
import image_rpi
import mqtt_rpi
import rest_rpi
import serial_rpi

IMAGE_PATH = os.path.join(os.getcwd(),'image')
CAMERA = camera_rpi.Camera_RPi()

def remove_all_image():
    list_file = os.listdir(IMAGE_PATH)
    for file in list_file:
        os.remove(os.path.join(IMAGE_PATH,file))
    print("Remove image")

def send_data(lock):
    if not lock.locked():
        lock.acquire()
        lock.release()
    # mouisture = serial_rpi.request_sensor_data()
    # filename = CAMERA.custom_capture(1,0)
    # CAMERA.start_preview()
    # time.sleep(2)
    # CAMERA.stop_preview()
    # os.remove(filename[0])
    # remove_all_image()
    # print(filename)

def main():
    lock = _thread.allocate_lock()
    mqtt_client = mqtt_rpi.Mqtt(send_data,lock)
    _thread.start_new_thread(mqtt_client.mqtt_loop,())
    while True:
        # mqtt_client.send_to_line(mqtt_rpi.GET_STR)
        time.sleep(600)
        send_data(lock)
    
if __name__ == '__main__':
    main()
