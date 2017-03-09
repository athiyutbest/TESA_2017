import serial
TTY = 'tty.usbmodem1423'


def request_sensor_data():
    data = None
    with serial.Serial('/dev/'+TTY,baudrate=115200,timeout=3) as ser:
        ser.write(b'r')
        data = int(ser.readline().decode('utf-8').strip(),16) 
    return data

