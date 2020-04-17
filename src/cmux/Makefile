CC=gcc
CFLAGS=-Wall
.PHONY: copy

all: diag cmux dev_name copy
	chmod +x ../bin/*

diag: DiagSaver.c tool.c tool.h
	gcc DiagSaver.c tool.c -o diag

program: cmux.c

clean:
	rm -f cmux

run: cmux
	../bin/cmux
copy:
	cp ./cmux ../bin/
	cp ./diag ../bin/

