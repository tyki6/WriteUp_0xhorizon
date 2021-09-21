# WriteUp KnowPlainText

Zip: https://ctf.0xhorizon.eu/files/knownPlainText.zip
On obient un text:
```
33a6bc400f4b760020b9a2732a0e6b4b04f9a01a2a0f29153e96be1d11413105
```

Et un fichier python:
```python
import os
from Crypto.Util.number import long_to_bytes
from Crypto.Util.strxor import strxor

FLAG = open("flag.txt", "rb").read()

key = os.urandom(8) * 20
c = strxor(FLAG, key[:len(FLAG)])
print(c.hex())
```

## Analyse

On vois que la key qui est utilisé est généré de façon aléatoire mais avec un cycle de 8 de longeur(ex: 123456781234567812345678etc...).
Ensuite on fait un xor ce c'est de chaine hexa.

Autre info capitale depuis le début du ctf tout nos flags commance par le mot **horiz0nx** information capitale car sa longeur fait 8 char parfait non?

## Trouver la Clé
On sait que la clé à un cycle de 8 char, et que les 8 premier char du flag.txt xoré au 8 premier char de clé font **horiz0nx**

Code:

```python
flag = "33a6bc400f4b760020b9a2732a0e6b4b04f9a01a2a0f29153e96be1d11413105"
debut_flag = b"horiz0nx"

flag_hex = bytes.fromhex(flag)
key = bytes(a ^ b for a,b in zip(debut_flag[:8], flag_hex[:8]))
print(key)
```

## Récupérer le flag
Une fois la clé trouvé, il nous faut alors refaire le programme tout simplement

Code:

```python
flag = "33a6bc400f4b760020b9a2732a0e6b4b04f9a01a2a0f29153e96be1d11413105"
debut_flag = b"horiz0nx"

flag_hex = bytes.fromhex(flag)
key = bytes(a ^ b for a,b in zip(debut_flag[:8], flag_hex[:8]))
key = key * 20
flag = bytes(a ^ b for a,b in zip(flag_hex, key[:len(flag_hex)]))
print(flag)
```
