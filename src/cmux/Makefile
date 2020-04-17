CC=gcc
CFLAGS=-Wall
.PHONY: copy

all: diag cmux dev_name copy
	chmod +x ../bin/*
	sed -i "s/\r//g" ../src/*
	sed -i "s/\r//g" ../cfg/net/*
	sed -i "s/\r//g" ../cfg/ppp/*
	chmod +x ../src/*
	chmod +x ../cfg/net/*
	chmod +x ../cfg/ppp/*

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
	cp ./cmux ../bin/
	cp ./diag ../bin/
	cp ./dev_name ../bin/