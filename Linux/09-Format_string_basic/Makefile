CC=gcc
CFLAGS=-I. -fno-stack-protector -fno-pie -no-pie 

all: auth

auth: auth.c
	$(CC) -o auth auth.c -m32 $(CFLAGS)

clean: auth 
	rm -f aut
