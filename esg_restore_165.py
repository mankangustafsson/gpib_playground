import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())
dev = rm.open_resource(
    "USB0::0x03EB::0x2065::Hewlett-Packard__ASG-A3000A__AA00000000__B.03.86::INSTR"
)
dev.read_termination = "\n"
dev.write_termination = "\n"
dev.query(":SYST:PRES; *OPC?;")
dev.write(":SERV:PRODUCTION:CAL:BEGIN;")
dev.write(":SERV:PRODUCTION:CAL 165,0,3.93400631533203125E7;")
dev.write(":SERV:PRODUCTION:CAL 165,1,50000.000000;")
dev.write(":SERV:PRODUCTION:CAL 165,2,4000000000.000000;")
dev.write(":SERV:PRODUCTION:CAL 165,5,7;")
dev.write(":SERV:PRODUCTION:CAL 165,6,8;")
dev.write(":SERV:PRODUCTION:CAL 165,7,5;")
dev.write(":SERV:PRODUCTION:CAL 165,8,9;")
dev.write(":SERV:PRODUCTION:CAL 165,10,4436.557800292969;")
dev.write(":SERV:PRODUCTION:CAL 165,12,8000000;")
dev.write(":SERV:PRODUCTION:CAL 165,13,8388608;")
dev.write(":SERV:PRODUCTION:CAL 165,20,1;")
dev.write(":SERV:PRODUCTION:CAL 165,21,4436.557800292969;")
dev.write(":SERV:PRODUCTION:CAL 165,24,3000;")
dev.write(":SERV:PRODUCTION:CAL:END;")
dev.write(":SERV:PRODUCTION:CAL:STORE 165;")
dev.write(":SERV:PRODUCTION:CAL:PUP;")
print("done, now restart your unit")
dev.close()
