import hashlib

def md5(data):
    md5 = hashlib.md5()
    if str:
        md5.update(data.encode(encoding='utf-8'))
    return md5.hexdigest()