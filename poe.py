import pyvisa

if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    dev = rm.open_resource('TCPIP0::192.168.1.181::1234::SOCKET')
    dev.timeout = 5000
    dev.read_termination = '\n'
    dev.write_termination = '\n'
    dev.write('++addr 13')
    dev.write('++auto 2')
    dev.write('++ifc')
    s = dev.query('*IDN?')
    print(f'connected to {s}')
    dev.close()
    rm.close()
