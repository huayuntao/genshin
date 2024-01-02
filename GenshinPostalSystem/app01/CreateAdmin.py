
import hashlib

def md5(data_string):
    str = 'django-insecure-6#5$)y*o+91&ut-!_10$0^93xi=)k*r$ezvz4v1oq%lgql)0+p'
    obj = hashlib.md5(str)
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()


md5('genshin_qidong')