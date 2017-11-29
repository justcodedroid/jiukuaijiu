# md5 加密
import  hashlib
from jiukuaijiy.settings import BASE_DIR
import  os
def fileToObj(filename):
    with open(filename,encoding='utf-8') as fr:
        return eval(fr.read())

provinces = fileToObj(os.path.join(BASE_DIR,'assets/province.json'))
citys = fileToObj(os.path.join(BASE_DIR,'assets/city.json'))
areas = fileToObj(os.path.join(BASE_DIR,'assets/area.json'))

#获得所有得市
def get_citys_by_id(provice_id):
    return citys[provice_id]
#获得所有得县
def get_areas_by_id(city_id):
    return areas[city_id]


#获得单个省
def get_province_one(provincesid):
    for data in provinces:
        if data['id'] == str(provincesid):
            return data['name']
#获得单个市
def get_city_one(provincesid,cityid):
    for data in citys:
        if data == str(provincesid):
            for data1 in citys[data]:
                if data1['id'] == str(cityid):
                    return data1['name']
#获得单个县
def get_area_one(cityid,areaid):
    for data in areas:
        if data == str(cityid):
            for data1 in areas[data]:
                if data1['id'] == str(areaid):
                    return data1['name']


def md5(text):
    md = hashlib.md5()
    md.update(text.encode())
    return md.hexdigest()

