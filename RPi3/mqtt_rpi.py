import os
import time
import signal
import queue
import urllib.parse as urlparse

import paho.mqtt.client as paho

GET_STR = '1'
SUBSCRIBE='line/call'
PUBLISH='line/back'


class Mqtt(paho.Client):
    def __init__(self, main_pid, q):
        super(Mqtt, self).__init__()

        def _on_message(mosq, obj, msg):
            print('Received Data : {}'.format(msg.payload))
            msg_str = msg.payload.decode('utf-8')
            if msg_str.lower().strip() == GET_STR:
                q.put(msg_str)
                os.kill(self.main_pid, signal.SIGUSR1)

        def _on_connect(mosq, obj, rc):
            print("Connected")

        def _on_publish(mosq, obj, mid):
            print("Send Data : mid = {}".format(mid))

        def _on_subscribe(mosq, obj, mid, granted_qos):
            print("Subscribed")

        self.main_pid = main_pid
        self.q = q
        self.on_message = _on_message
        self.on_connect = _on_connect
        self.on_publish = _on_publish
        self.on_subscribe = _on_subscribe
        url_str = os.environ.get(
            'CLOUDMQTT_URL', 'mqtt://alrldpua:9G_mZAtkY50u@m11.cloudmqtt.com:15303')
        url = urlparse.urlparse(url_str)
        self.username_pw_set(url.username, url.password)
        self.connect(url.hostname, url.port)
        self.subscribe(SUBSCRIBE, 0)

    def send_to_line(self, msg):
        self.publish(PUBLISH, msg)

    def mqtt_loop(self):
        while True:
            self.loop()
