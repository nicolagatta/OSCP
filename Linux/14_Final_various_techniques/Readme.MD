test		compiled on Ubuntu 18.04 with gcc 7.5.0
training:	compiled on kali 2022 with gcc-12

The difference is that gcc-12 on kali is missing "pop rdi; ret" gadget in the executable.
So it's not possible to execute the first phase of exploit leaking the address of puts
