CC=gcc
CFLAGS= -g -Wall -pipe -Os -std=gnu99

all: bin2eeprom eeprom2bin eprom2bin myhexdump

clean:
	rm -f bin2eeprom eeprom2bin eprom2bin myhexdump
