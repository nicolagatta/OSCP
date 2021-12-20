A Sample stack canary bypass example

This example is very peculiar and the prerequisites are specific to this vulnerable program
- executes two read() (and not gets())
- print the output at every execution of read
- has an helper function that executes system("/bin/sh")

This lead to a leak of the stack canary in the first iteration, use the canary value in the second iteration and return to system("/bin/sh")

Compile with:
gcc -m32 -no-pie vulnerable.c -o vulnerable -fstack-protector