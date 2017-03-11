import os
import queue
import signal
import time
import requests
import json
import _thread
import camera_rpi
import image_rpi
import mqtt_rpi
import rest_rpi
import serial_rpi


CAMERA = camera_rpi.Camera_RPi()
INTERVAL = 600
Queue = queue.Queue(2)
Lock = _thread.allocate_lock()


def handler(signum, frame):
    command = int(Queue.get())
    if command == 1:
        send_data()
    else:
        print("Error : Command not found")


def get_geo():
    res = requests.get('https://freegeoip.net/json/')
    json_res = json.loads(res.text)
    return json_res


def send_data():
    if not Lock.locked():
        Lock.acquire()
        image_rpi.remove_all_image()
        moisture = 99
        # moisture = serial_rpi.request_sensor_data()
        CAMERA.custom_capture(1, 0)
        image_rpi.resize_image(image_rpi.get_image()[0])
        data = {}
        list_image = image_rpi.get_image()
        if '_preview' in list_image[1]:
            data = rest_rpi.create_data(
                moisture, list_image[0], list_image[1])
        else:
            data = rest_rpi.create_data(
                moisture, list_image[1], list_image[0])
        result = rest_rpi.post_data(data)
        if result.status_code == 200:
            print('Succ : send_data')
        else:
            print('Error : send_data({})'.format(result.status_code))
        Lock.release()


def main():
    signal.signal(signal.SIGUSR1, handler)
    mqtt_client = mqtt_rpi.Mqtt(os.getpid(), Queue)
    _thread.start_new_thread(mqtt_client.mqtt_loop, ())
    while True:
        time.sleep(INTERVAL)
        send_data()


if __name__ == '__main__':
    main()
