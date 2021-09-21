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
print(message)
print(res)
print(math.sqrt(res))
print(round(math.sqrt(res), 2))
conn.send(f'{round(math.sqrt(res), 2)}\r\n')
print(conn.recvline())