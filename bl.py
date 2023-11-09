import sys
import os
import serial
import time
import binascii
import struct
import math


baud = 115200

def poll_RX():
    buf = ser.read(11)
    if len(buf) == 11:
        if (buf[0]==36) and (buf[1]==70) and (buf[2]==54) and (buf[9]==13) and (buf[10]==10):
            if(dest==(binascii.unhexlify((buf[3].to_bytes(length=1,byteorder='big', signed=False))+(buf[4].to_bytes(length=1,byteorder='big', signed=False))))):
                Ecode = (binascii.unhexlify((buf[7].to_bytes(length=1,byteorder='big', signed=False))+(buf[8].to_bytes(length=1,byteorder='big', signed=False))))
                if(Ecode[0] == 0):
                    return(True)
                else:
                    print("Resp, Error ",'{:0>2X}'.format(Ecode[0]))
                    return(False)
            else:
                print("Resp, Wrong ID")
                return(False)
        else:
            print("Resp, Bad Packet")
            return(False)
    else:
        print("Resp, Timeout")
        return(False)


def GoToBoot():
    for y in range(30):
        ser.write(b'$')
        ser.write(binascii.hexlify(dest).upper())
        ser.write(b'F800000000\r\n') #GoToBoot
        for x in range(10):
            while (ser.inWaiting()>0):
                chr = ser.read(1)
                if(chr == b'$'):
                    buf = ser.read(10)
                    if(len(buf) == 10):
                        if ((buf[0]==70) and (buf[1]==54) and (buf[8]==13) and (buf[9]==10)):
                            print("Ok")
                            return(True)
            time.sleep(0.01)
    print("Timeout")
    return(False)


def sendreq(TID):
    ser.write(b'$')
    ser.write(binascii.hexlify(TID.to_bytes(length=1,byteorder='big', signed=False)).upper())
    ser.write(b'F800000000\r\n') #GoToBoot
    for x in range(3):
        while (ser.inWaiting()>0):
            chr = ser.read(1)
            if(chr == b'$'):
                buf = ser.read(10)
                if(len(buf) == 10):
                    if ((buf[0]==70) and (buf[1]==54) and (buf[8]==13) and (buf[9]==10)):
                        return(True)
        time.sleep(0.01)
    return(False)


def Scan():
    for z in range(63):
        z+=128
        NotFound = True
        for y in range(3):
            if(NotFound):
                if(sendreq(z)):
                    NotFound = False
        if(NotFound):
            print('{:0>2X}'.format(z),":. ", end='', sep='')
        else:
            print('{:0>2X}'.format(z),":X ", end='', sep='')
        if((z%8)==7):
            print(" ")


def data_RX():
    buf = ser.read(519)
    if(len(buf) == 519):
        if (buf[0]==36) and (buf[1]==70) and (buf[2]==55) and (buf[517]==13) and (buf[518]==10):
            if(dest==(binascii.unhexlify((buf[3].to_bytes(length=1,byteorder='big', signed=False))+(buf[4].to_bytes(length=1,byteorder='big', signed=False))))):
                Ecode = (binascii.unhexlify((buf[7].to_bytes(length=1,byteorder='big', signed=False))+(buf[8].to_bytes(length=1,byteorder='big', signed=False))))
                #i=9
                dbuf = binascii.unhexlify(buf[5:517])
                #dbuf = buf[i:i+2]
                #print(dbuf)
                frd.write(dbuf);
                return(True)
            else:
                print("RX, Wrong ID")
                return(False)
        else:
            print("RX, Bad Packet")
            return(False)
    else:
        print("RX, Timeout")
        return(False)

def Enable():
    ser.write(b'$')
    ser.write(binascii.hexlify(dest).upper())
    ser.write(b'F0') #Enable
    addr_lsb, addr_msb = struct.pack('<H', addr)
    ser.write(binascii.hexlify(addr_msb.to_bytes(length=1,byteorder='big', signed=False)).upper())
    ser.write(binascii.hexlify(addr_lsb.to_bytes(length=1,byteorder='big', signed=False)).upper())
    ser.write(b'0000') #pad
    ser.write(b'\r\n')
    if(poll_RX() == False):
        print("Enable Fail")
        sys.exit()


def Read_data():
    ser.write(b'$')
    ser.write(binascii.hexlify(dest).upper())
    ser.write(b'F1') #Read
    addr_lsb, addr_msb = struct.pack('<H', addr)
    ser.write(binascii.hexlify(addr_msb.to_bytes(length=1,byteorder='big', signed=False)).upper())
    ser.write(binascii.hexlify(addr_lsb.to_bytes(length=1,byteorder='big', signed=False)).upper())
    ser.write(b'0000') #pad
    ser.write(b'\r\n')
    if(data_RX() == False):
        print("Read Fail")
        sys.exit()


def Verify_data():
    File_active=True
    First=True
    for x in range(256):
        if (byte := f.read(1)):
            if(First):
                First=False
                ser.write(b'$')
                ser.write(binascii.hexlify(dest).upper())
                ser.write(b'F5') #Verify
                addr_lsb, addr_msb = struct.pack('<H', addr)
                ser.write(binascii.hexlify(addr_msb.to_bytes(length=1,byteorder='big', signed=False)).upper())
                ser.write(binascii.hexlify(addr_lsb.to_bytes(length=1,byteorder='big', signed=False)).upper())
            ser.write(binascii.hexlify(byte).upper())
        else:
            if(First):
                return(False)
            ser.write(binascii.hexlify(b'\0').upper())
            File_active=False
    ser.write(b'\r\n')
    if(poll_RX() == False):
        print("Verify Fail")
        sys.exit()
    return(File_active)


def Launch():
    ser.write(b'$')
    ser.write(binascii.hexlify(dest).upper())
    ser.write(b'F2') #Launch
    addr_lsb, addr_msb = struct.pack('<H', addr)
    ser.write(binascii.hexlify(addr_msb.to_bytes(length=1,byteorder='big', signed=False)).upper())
    ser.write(binascii.hexlify(addr_lsb.to_bytes(length=1,byteorder='big', signed=False)).upper())
    ser.write(b'0000') #pad
    ser.write(b'\r\n')


def Send_data(modifier):
    File_active=True
    First=True
    strippedID=(dest[0] & 0x7f)
    hx_ID = binascii.hexlify(strippedID.to_bytes(length=1,byteorder='big', signed=False)).upper()
    inv_ID = binascii.hexlify((255-strippedID).to_bytes(length=1,byteorder='big', signed=False)).upper()
    for x in range(256):
        if (byte := f.read(1)):
            if(First):
                First=False
                Enable()
                ser.write(b'$')
                ser.write(binascii.hexlify(dest).upper())
                ser.write(b'F4') #Prog
                addr_lsb, addr_msb = struct.pack('<H', addr)
                ser.write(binascii.hexlify(addr_msb.to_bytes(length=1,byteorder='big', signed=False)).upper())
                ser.write(binascii.hexlify(addr_lsb.to_bytes(length=1,byteorder='big', signed=False)).upper())
            if((x == modifier) and (modifier !=0)):
                ser.write(hx_ID)
            elif((x == (modifier+1)) and (modifier !=0)):
                ser.write(inv_ID)
            else:
                ser.write(binascii.hexlify(byte).upper())
        else:
            if(First):
                return(False)
            ser.write(binascii.hexlify(b'\0').upper())
            File_active=False
    ser.write(b'\r\n')
    if(poll_RX() == False):
        print("Write Fail")
        sys.exit()
    return(File_active)


def Erase_data():
    Enable()
    ser.write(b'$')
    ser.write(binascii.hexlify(dest).upper())
    ser.write(b'F3') #Erase
    addr_lsb, addr_msb = struct.pack('<H', addr)
    ser.write(binascii.hexlify(addr_msb.to_bytes(length=1,byteorder='big', signed=False)).upper())
    ser.write(binascii.hexlify(addr_lsb.to_bytes(length=1,byteorder='big', signed=False)).upper())
    fblock_lsb, fblock_msb = struct.pack('<H', fblock)
    ser.write(binascii.hexlify(fblock_msb.to_bytes(length=1,byteorder='big', signed=False)).upper())
    ser.write(binascii.hexlify(fblock_lsb.to_bytes(length=1,byteorder='big', signed=False)).upper())
    ser.write(b'\r\n')
    if(poll_RX() == False):
        print("Erase Fail")
        sys.exit()

if len(sys.argv) != 6:
    print("Argument description 'Port File    ID Addr Operation'")
    print("Argument example     'COM5 fil.bin 8C ABCD w'")
    sys.exit()
for i, arg in enumerate(sys.argv):
    if i==1:
        port = arg
        ser = serial.Serial(port, baud, timeout=3)
        print("Port ",port)
    if i==2:
        file = arg
        f =open(file, "rb")
        fsize = os.path.getsize(file)
        fblock = math.ceil(fsize/256)
        print("File ",file,"size",fsize,"Block",fblock)
    if i==3:
        dest = binascii.unhexlify(arg)
        print("DestID ",'{:0>2X}'.format(dest[0]))
    if i==4:
        start = binascii.unhexlify(arg)
        addr = start[0]*256+start[1]
        print("Addr ",'{:0>4X}'.format(addr))
    if i==5:
        operation = arg
        print("Operation ",operation)

if (operation == 'w'):
    while (Send_data(0)):
        addr += 1
elif (operation == 'i'):
    modifier = 0xbc
    while (Send_data(modifier)):
        addr += 1
        modifier = 0
elif (operation == 'e'):
    Erase_data()
elif (operation == 'v'):
    while (Verify_data()):
        addr += 1
elif (operation == 'l'):
    Launch()
elif (operation == 'r'):
    frd =open(file+'.rb', "wb")
    for readblock in range(fblock):
        Read_data()
        addr += 1
    frd.close()
elif (operation == 'b'):
    GoToBoot()
elif (operation == 's'):
    Scan()
else:
    print("Argument description 'Port File    ID Addr Operation'")
    print("Argument example     'COM5 fil.bin 8C ABCD w'")

# while (True):
#     if (ser.inWaiting()>0):
#         print(ser.read(ser.inWaiting()))
#     time.sleep(0.01)
f.close()
