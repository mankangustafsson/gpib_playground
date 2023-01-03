from RfGen import RfGen
from Devices import *
from Probe import *

rf = Lab.connectByType(Device.Type.RF_GEN)
rf.query(':SYST:PRES; *OPC?')

pm = Lab.connectByType(Device.Type.POWER_METER, False)
probe = probes[0] # HP8481A, sensor A

# update frequency index
#rf.write(':SERV:PROD:CAL:BEGIN')
#i = 62
#for idx in range(81, 142):
#for f in range(2940, 4020, 60):
#    rf.write(f'SERV:PROD:CAL 65,{idx},{4019 * 1e6}')
#    i = i + 1
#i = 80
#f = 4019
#rf.write(f'SERV:PROD:CAL 65,{i},{f * 1e6}')
#rf.write(f'SERV:PROD:CAL 65,{i+1},{f * 1e6}')
#rf.write(':SERV:PROD:CAL:END')
#rf.write(':SERV:PROD:CAL:STORE 65')
#rf.write(':SERV:PROD:CAL:PUP')
#rf.query(':SYST:PRES; *OPC?')

# dump current settings
#for idx in range(0, 142):
#for idx in range(62, 83):
#    freq = float(rf.query(f':SERV:PROD:CAL? 65,{idx}'))
#    offset = float(rf.query(f':SERV:PROD:CAL? 207,{idx}'))
#    print(f'Index: {idx:3} Frequency: {freq/1000000:11.6f} MHz = {offset:5.2f} dBm')
#
#print()

# zero settings 62/2940MHz..80/4000MHz
#rf.write(':SERV:PROD:CAL:BEGIN')
#for idx in range(78, 83):
#    rf.write(f':SERV:PROD:CAL 207,{idx},0')
#rf.write(':SERV:PROD:CAL:END')
#rf.write(':SERV:PROD:CAL:STORE 207')
#rf.write(':SERV:PROD:CAL:PUP')

#rf.query(':SYST:PRES; *OPC?')

for idx in range(78, 83):
    freq = float(rf.query(f':SERV:PROD:CAL? 65,{idx}'))
    offset = float(rf.query(f':SERV:PROD:CAL? 207,{idx}'))
    print(f'Index: {idx:3} Frequency: {freq/1000000:11.6f} MHz = {offset:5.2f} dBm')

print()

# collect cal data
caldata = []
for idx in range(78, 83):
    freq = float(rf.query(f':SERV:PROD:CAL? 65,{idx}'))
    rf.write(f'*CLS; :STAT:QUES:POW:ENAB 32767; :STAT:QUES:ENAB 32767; :OUTP:MOD OFF; :FREQ:CW {freq/1e6} MHz; :POWER 0 dBm; :OUTP ON')
    time.sleep(0.8)
    cf = probe.get_cf(freq)
    pmCommand = 'AE KB%.1fEN LG RL0 AP TR2 TR3' %cf
    reply = pm.query_ascii_values(pmCommand)
    offset = float(reply[0])
    print(f'Index: {idx:3} Frequency: {freq/1000000:11.6f} MHz = {offset:5.2f} dBm')
    caldata.append({"index":idx, "offset":offset})

rf.write(':OUTP OFF')

# write caldata
#rf.write(':SERV:PROD:CAL:BEGIN')

#for e in caldata:
#    rf.write(f':SERV:PROD:CAL 207,{e["index"]},{-e["offset"]:5.2f}')
#    print(f':SERV:PROD:CAL 207,{e["index"]},{e["offset"]:5.2f}')
#rf.write(':SERV:PROD:CAL:END')
#rf.write(':SERV:PROD:CAL:STORE 207')
#rf.write(':SERV:PROD:CAL:PUP')
#
#rf.query(':SYST:PRES; *OPC?')

print('Done')    
pm.close()
rf.close()

