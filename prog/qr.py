import os
from PIL import Image
from pyzbar.pyzbar import decode
arr = os.listdir("qr")
s = ""
for img in arr:
    data = decode(Image.open("qr/" + img))
    print(data)
    s += data[0].data.decode()
print(s)