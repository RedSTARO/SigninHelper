import hashlib
a = hashlib.md5()
a.update(str(365* 188043 * 41227).encode('utf-8'))
print(a.hexdigest())
