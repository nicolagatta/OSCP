This is an.example of bypassing ASLR and NX protection on x86

The vulnerable application "pwn3" is a sample from https://github.com/mishrasunny174/encrypt-ctf/tree/master/pwn/x86/pwn3 

Setup: 
- NX:             enabled
- ASLR:           enabled
- Stack canary:   disabled

It can be exploited with a standard input > 140 bytes

The exploit uses ret2libc to 
- perform a first exploitation using puts() and main() to leak address of puts at runtime 
- re-executing main() 
- calculate the position in memory of system() exit() and "/bin/sh" using offsets already know by gdb
- exploiting by chaining system() + exit() + "/bin/sh"

vulnerable binary can be run on tcp port 444 using: "socat TCP-LISTEN:4444,reuseaddr,fork EXEC:./pwn3"