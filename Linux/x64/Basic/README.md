# Basic vulnerable program with no ASLR, no NX and no Stack Canary

exploit.py should be modified according to the specific memory address the shellcode is put on the stack

It uses gets() so we need a little trick
$ exploit.py > input
$ (cat input; cat)| ./basic