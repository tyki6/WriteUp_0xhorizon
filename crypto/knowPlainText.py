flag = "33a6bc400f4b760020b9a2732a0e6b4b04f9a01a2a0f29153e96be1d11413105"
debut_flag = b"horiz0nx"

flag_hex = bytes.fromhex(flag)
key = bytes(a ^ b for a,b in zip(debut_flag[:8], flag_hex[:8]))
key = key * 20
flag = bytes(a ^ b for a,b in zip(flag_hex, key[:len(flag_hex)]))
print(flag)