# PIE means that the executable is loaded at random memory position (when ASLR is enabled)
# This make ineffective the usual ASLR leak technique of 
# - executing a ret2lib chain: puts() + main() + puts.plt
# - leaking puts address after ASLR effects
# - calculate offsets in libc of system(), /bin/sh, exit(), pop rdi gadget 
# - returning to main() to perform a second overflow using correct address

# When PIE is enabled there can be other ways like
# - format strings that leaks the address the code segment is stored in memory 
# - use offset to get the address of puts(), main() and puts.plt
# - execute again the above  technique  

