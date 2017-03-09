import picamera,time,json,os.path,datetime

SETTINGS = ['sharpness','contrast','brightness','saturation','ISO'
    ,'video_stabilization','exposure_compensation','exposure_mode'
    ,'meter_mode','awb_mode','image_effect','color_effects','rotation'
    ,'hflip','vflip','crop']
IMAGE_PATH = os.path.join(os.getcwd(),'image')
SETTINGS_FILE_PATH = os.path.join(os.getcwd(),'camera_setting.json')

class Camera_RPi(picamera.PiCamera):
    def __init__(self,default_setting=False):
        super(Camera_RPi,self).__init__()
        if not os.path.isfile(SETTINGS_FILE_PATH) or default_setting:
            self.save_setting()
        else:
            self.load_setting()
    
    def save_setting(self):
        with open(SETTINGS_FILE_PATH,'w') as file:
            tmp_setting = {}
            for attr in SETTINGS:
                tmp_setting[attr] = getattr(self, attr)
            json.dump(tmp_setting,file)
    
    def load_setting(self):
        with open(SETTINGS_FILE_PATH,'r') as file:
                data = json.load(file)
                for attr in SETTINGS:
                    setattr(self,attr,data[attr])
        
    def show_settings(self):
        for attr in SETTINGS:
            print('{} {} : {}'.format(SETTINGS.index(attr),attr,getattr(self, attr)))

    def preview(self):
        self.start_preview(fullscreen=False,window=(0,0,640,480))
        show_settings(self)
        print('Press Ctrl + C to exit.')
        try:
            while True:
                in_command = input('Enter number of setting :')
                in_vaule = input('Enter value of setting :')
                setattr(self,SETTINGS[int(in_command)],type(getattr(self,SETTINGS[int(in_command)]))(in_vaule)) 
        except KeyboardInterrupt:
            save_str = input('\nSave(y/n) : ')
            if save_str.lower() == 'y':
                save_setting(self)
            else:
                load_setting(self)
            self.stop_preview()

    def load_default(self):
        self.__init__(default_setting=True)

    def custom_capture(self,num=3,delay=0):
        filenames = [os.path.join(IMAGE_PATH ,'image%02d' % i+datetime.datetime.now().strftime('(%d-%m-%y-%H:%M:%S)')+'.jpg') for i in range(num)]
        print('Capturing...')
        for name in filenames:
            self.capture(name,resize=(1024,1024))
            time.sleep(delay)
        return filenames
        