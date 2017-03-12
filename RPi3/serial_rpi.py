import serial
TTY = 'ttyACM0'


def request_sensor_data():
    data = None
    with serial.Serial('/dev/'+TTY,baudrate=115200,timeout=3) as ser:
        try:
            ser.write(b'r')
            data = int(ser.readline().decode('utf-8').strip(),16) 
            return data
        except :
            return -1
        

