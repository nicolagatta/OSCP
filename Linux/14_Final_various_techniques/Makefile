CC=gcc
CFLAGS=-I. -fno-stack-protector -fno-pie -no-pie 

all: vuln-32 vuln-64

vuln-32: training.c
	$(CC) -o vuln-32 training.c -m32 $(CFLAGS)

vuln-64: training.c
	$(CC) -o vuln-64 training.c $(CFLAGS)

clean: vuln-32 vuln-64 
	rm -f vuln-32 vuln-64
