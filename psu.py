from Devices import Device, Lab


if __name__ == "__main__":
    dev = Lab.connectByType(Device.Type.PSU, verbose=True)
    if dev is None:
        exit(1)
    dev.write('APPLY P6V, 4.5,0.2')
    dev.write('APPLY P25V,10,0.3')
    dev.write('OUTPUT:STATE ON')
    dev.write('OUTPUT:TRACK:STATE ON')
