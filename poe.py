import pyvisa
# import time

if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    #    print(rm.list_resources())
    dev = rm.open_resource("TCPIP0::192.168.1.181::inst13::INSTR")
    dev.timeout = 5000
    dev.read_termination = "\n"
    dev.write_termination = "\n"
    #    dev.write('++addr 13')
    #    dev.write('++auto 2')
    #    dev.write('++ifc')
    s = dev.query("*IDN?")
    print(f"connected to {s}")
    #    time.sleep(10)
    dev.close()
    rm.close()
