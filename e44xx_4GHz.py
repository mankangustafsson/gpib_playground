from Devices import *

dev = Lab.connectByType(Device.Type.RF_GEN)
dev.query(':SYST:PRES; *OPC?;')
input('This will change EEPROM settings to enable 4GHz output and lower limit to 50kHz')
print('4GHz upgrade in progress...', end = '', flush = True)
dev.write(':SERV:PRODUCTION:CAL:BEGIN;')
dev.write(':SERV:PRODUCTION:CAL 165,1,50000.000000;')
dev.write(':SERV:PRODUCTION:CAL 165,2,4000000000.000000;')
dev.write(':SERV:PRODUCTION:CAL:END;')
dev.write(':SERV:PRODUCTION:CAL:STORE 165;')
dev.write(':SERV:PRODUCTION:CAL:PUP;')
print('done, now restart your unit')
dev.close()
