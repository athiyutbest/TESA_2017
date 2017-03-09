import os
import time,signal,queue
from pprint import pprint

import _thread
import camera_rpi
import image_rpi
import mqtt_rpi
import rest_rpi
import serial_rpi

IMAGE_PATH = os.path.join(os.getcwd(),'image')
CAMERA = camera_rpi.Camera_RPi()
INTERVAL = 600
Queue = queue.Queue()
Lock = _thread.allocate_lock()

def handler(signum,frame):
    if int(Queue.get()) == 1:
        send_data()

def remove_all_image():
    list_file = os.listdir(IMAGE_PATH)
    for file in list_file:
        os.remove(os.path.join(IMAGE_PATH,file))
    print("Remove image")

def get_image():
    list_image = os.listdir(IMAGE_PATH)
    tmp = []
    for image in list_image:
        image = os.path.join(IMAGE_PATH,image)
        tmp.append(image)
    return tmp

def send_data():
    if not Lock.locked():
        Lock.acquire()
        remove_all_image()
        moisture = 99
        # moisture = serial_rpi.request_sensor_data()
        images = CAMERA.custom_capture(1,0)
        image_rpi.resize_image(get_image()[0])
        data = {}
        tmp_list_image = get_image()
        if  '_preview' in tmp_list_image[1]:
            data = rest_rpi.create_data(moisture,tmp_list_image[0],tmp_list_image[1])
        else:
            data = rest_rpi.create_data(moisture,tmp_list_image[1],tmp_list_image[0])
        result = rest_rpi.post_data(data)
        if result.status_code == 200:
            print('Successful')    
        else :
            print('ERR : {}'.format(result.status_code))
        Lock.release()

def main():
    signal.signal(signal.SIGUSR1,handler)
    mqtt_client = mqtt_rpi.Mqtt(os.getpid(),Queue)
    _thread.start_new_thread(mqtt_client.mqtt_loop,())
    while True:
        # time.sleep(3)
        # mqtt_client.send_to_line(mqtt_rpi.GET_STR)
        time.sleep(INTERVAL)

    
if __name__ == '__main__':
    main()
    