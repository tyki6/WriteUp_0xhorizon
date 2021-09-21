# WriteUp Qrcode

Lien des resources: https://ctf.0xhorizon.eu/files/qr.gif

On voit un gif avec un ensemble de qr code qui ce suivent.On va essayer de tous les decoder.

## Transformer notre gif en une liste d'images

Grâce à https://ezgif.com/split on peut découper un gif en image.
Une fois que l'on a tous nos qr code dans un dossier il nous faut tous les analyser.

## Decoder un qr Code
Pour analysé un qrcode j'ai choisit d'utiliser zbar (lib open source pour la lecture de qrcode) et PIL(lib python de traitement d'image)

Installation:
```bash
pip install PIL
sudo apt-get install libzbar0
pip install pyzbar
```

Code:
```python
import os
from PIL import Image
from pyzbar.pyzbar import decode
arr = os.listdir("qr")
for img in arr:
    data = decode(Image.open("qr/" + img))
    print(data)
```

Resultat:
```
[Decoded(data=b'h', type='QRCODE', rect=Rect(left=40, top=40, width=210, height=210), polygon=[Point(x=40, y=40), Point(x=40, y=250), Point(x=250, y=250), Point(x=250, y=40)])]
[Decoded(data=b'o', type='QRCODE', rect=Rect(left=40, top=40, width=210, height=210), polygon=[Point(x=40, y=40), Point(x=40, y=250), Point(x=250, y=250), Point(x=250, y=40)])]
...
[Decoded(data=b't', type='QRCODE', rect=Rect(left=40, top=40, width=210, height=210), polygon=[Point(x=40, y=40), Point(x=40, y=250), Point(x=250, y=250), Point(x=250, y=40)])]
[Decoded(data=b'}', type='QRCODE', rect=Rect(left=40, top=40, width=210, height=210), polygon=[Point(x=40, y=40), Point(x=40, y=250), Point(x=250, y=250), Point(x=250, y=40)])]
```

On voit que chaque qrcode à dans le champ data une lettre du flag, il nous suffit de tous les assembler pour avoir le flag final.

## Code Final

Code:
```python
import os
from PIL import Image
from pyzbar.pyzbar import decode
arr = os.listdir("qr")
s = ""
for img in arr:
    data = decode(Image.open("qr/" + img))
    s += data[0].data.decode()
print(s)
```