import pprint

import requests

def create_data(moisture,image,image_preview):
    data = {}
    data['moisture'] = moisture
    data['image'] = open(image,'rb')
    data['image_preview'] = open(image_preview,'rb')
    return data

def get_all():
    return requests.get('https://supapich2db.herokuapp.com/sup/sensor/all/').json()

def post_data(data):
    file = {}
    file['image'] = data['image']
    file['image_preview'] = data['image_preview']
    data_tmp = {}
    data_tmp['moisture'] = data['moisture']
    return requests.post('https://supapich2db.herokuapp.com/sup/up',data=data_tmp,files=file,headers={'enctype':'multipart/form-data'})
