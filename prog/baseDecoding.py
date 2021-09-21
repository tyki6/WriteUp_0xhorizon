import base64
import re

from pwnlib.tubes.remote import remote
conn = remote('0xhorizon.eu',9999)
message = conn.recvuntil(': ', drop=True).decode()
regex = r".* \('(?P<base>.*)'\).*"
m = re.match(regex, message)
if m:
    text = m.group("base")
    while True:
        try:
            text = base64.b64decode(text)
        except:
            break
    regex = r".*: (?P<password>.*)"
    password = re.match(regex, text.decode()).group("password")
    print(message)
    print(password)
    conn.send(password.encode() + b'\r\n')
    print(conn.recvline())