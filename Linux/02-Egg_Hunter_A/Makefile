CC=gcc
CFLAGS=-I. -fno-stack-protector -fno-pie -no-pie -m32 -zexecstack

all: shell_bind egg_hunter

egg_hunter: egg_hunter.c
	$(CC) -o egg_hunter egg_hunter.c -m32 $(CFLAGS)

shell_bind: shell_bind.c
	$(CC) -o shell_bind shell_bind.c $(CFLAGS)
