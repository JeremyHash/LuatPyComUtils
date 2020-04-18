CC=gcc
CFLAGS=-Wall
.PHONY: copy

all: diag cmux dev_name copy
	chmod +x ../bin/*

diag: DiagSaver.c tool.c tool.h
	gcc DiagSaver.c tool.c -o diag

dev_name: dev_name.c tool.c tool.h
	gcc dev_name.c tool.c -o dev_name

program: cmux.c

clean:
	rm -f cmux

run: cmux
	../bin/cmux
copy:
	mv ./cmux ../bin/
	mv ./diag ../bin/
	mv ./dev_name ../bin/

