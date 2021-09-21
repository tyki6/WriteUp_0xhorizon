# WriteUp Math

## Lancer le challenge

commande: `nc 0xhorizon.eu 7777`

résultat:

```bash
Please return the square root of this calculus round two decimals... 2 seconds max^^

1202 * 523

?> 
```

On va donc faire un programme simple pour récuperer l'opération et après renvoyer la racine carré arrondie à deux décimales.On remarque aussi que le message nous demande toujours de faire la racine carré (pas besoin d'analyser la phrase donc.)

## Se connecter au challenge avec Python

Pour génér la connexion, la lecture et l'envoie de message: on utilise le paquet `pwntools`

installation: `pip install pwntools`
Code:

```python
from pwn import *

r = remote('0xhorizon.eu', 9999) #se connecter
message = conn.recvuntil('>', drop=True).decode() # récuperer la phrase de départ
print(message)
```

## Analyser l'opération

Une bonne vieille regex avec l'aide de [regex101](https://regex101.com/).

On se retrouve avec `".*\n\n(?P<first>\d+) (?P<op>.+) (?P<second>\d+).*"`

Decortiquons la regex:

- `".*\n\n`: Pour la **phrase qui est présent** tout le temps.
- `(?P<first>\d+)`: pour la **premiere partie** de l'opération
- `(?P<op>.+)`: pour le **type** d'opération à faire
- `(?P<second>\d+)`: pour la **seconde partie** de l'opération
- `.*`: pour le reste (on s'en fou)

Code:

```python
from pwn import *
import re
conn = remote('0xhorizon.eu',7777)
message = conn.recvuntil('>', drop=True).decode()
regex = r".*\n\n(?P<first>\d+) (?P<op>.+) (?P<second>\d+).*"
m = re.match(regex, message)
```

## Calculer l'opération

Grâce à notre regex on a juste à faire un if pour chaque opération et après faire un bon sqrt et round pour avoir le resultat.

Code:

```python
from pwn import *
import re
conn = remote('0xhorizon.eu',7777)
message = conn.recvuntil('>', drop=True).decode()
regex = r".*\n\n(?P<first>\d+) (?P<op>.+) (?P<second>\d+).*"
m = re.match(regex, message)
if m:
    first = int(m.group("first"))
    second = int(m.group("second"))
    if m.group("op") == "+":
        res = first + second
    if m.group("op") == "-":
        res = first - second
    if m.group("op") == "*":
        res = first * second
    if m.group("op") == "/":
        res = first / second
    res = round(math.sqrt(res), 2)
```

## Code final

```python
from pwn import *
import re
conn = remote('0xhorizon.eu',7777)
message = conn.recvuntil('>', drop=True).decode()
regex = r".*\n\n(?P<first>\d+) (?P<op>.+) (?P<second>\d+).*"
m = re.match(regex, message)
if m:
    first = int(m.group("first"))
    second = int(m.group("second"))
    if m.group("op") == "+":
        res = first + second
    if m.group("op") == "-":
        res = first - second
    if m.group("op") == "*":
        res = first * second
    if m.group("op") == "/":
        res = first / second
    res = round(math.sqrt(res), 2)
    conn.send(f'{res}\r\n') # ne pas oublier \r\n à la fin de la réponse.
    print(conn.recvline()) # récupérer le flag.
```
