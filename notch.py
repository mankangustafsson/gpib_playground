import argparse
import binascii

from quantiphy import Quantity, QuantityError
import serial


def valid_frequency(f):
    try:
        frequency = round(Quantity(f, 'Hz') / 1E6)
        if frequency < 0 or frequency > 65535:
            raise ValueError(frequency)
        return frequency
    except QuantityError:
        msg = '%s is not a valid frequency' % f
        raise argparse.ArgumentTypeError(msg)


def valid_address(a):
    if a > 0 and a < 63:
        return a
    else:
        msg = '%d is not a valid address' % a
        raise argparse.ArgumentTypeError(msg)


def valid_register(r):
    if r >= 0 and r <= 65535:
        return r
    else:
        msg = '%d is not a valid register' % r
        raise argparse.ArgumentTypeError(msg)


def SendCommand(cardId, senderId, register, value):
    port.write(b'$')
    port.write(binascii.hexlify(cardId.to_bytes(length=1, byteorder='big',
                                                signed=False).upper()))
    port.write(binascii.hexlify(senderId.to_bytes(length=1, byteorder='big',
                                                  signed=False).upper()))
    port.write(binascii.hexlify(register.to_bytes(length=2, byteorder='big',
                                                  signed=False).upper()))
    port.write(binascii.hexlify(value.to_bytes(length=2, byteorder='big',
                                               signed=False).upper()))
    port.write(b'\r\n')

    r = port.read(11)
    print(r)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default='COM37',
                        metavar='COM-port',
                        help='COM port to use')
    parser.add_argument('-l', type=valid_frequency, default=0,
                        metavar='low-frequency',
                        help='frequency to use for low filter '
                        'Decimal values with suffixes k, M and G is also'
                        ' allowed, internally converted to integer MHz')
    parser.add_argument('-b', type=valid_frequency, default=0,
                        metavar='high-frequency',
                        help='frequency to use for high filter '
                        'Decimal values with suffixes k, M and G is also'
                        ' allowed, internally converted to integer MHz')
    parser.add_argument('-al', type=valid_address, default=1,
                        metavar='low-address',
                        help='bus address to use for low filter')
    parser.add_argument('-ab', type=valid_address, default=2,
                        metavar='high-address',
                        help='bus address to use for high filter')
    parser.add_argument('-r', type=valid_register, default=0,
                        metavar='write to register',
                        help='register, do not use this!')

    args = parser.parse_args()
    # print(args)

    if args.al == args.ab:
        raise ValueError('Low and high address cannot be equal: %d' % args.al)

    senderAddress = max(args.al, args.ab) + 1
    if senderAddress >= 63:
        senderAddress = 0

    port = serial.Serial(args.p, 115200, timeout=3)

    if args.l != 0:
        SendCommand(args.al | 0x40, senderAddress | 0x40, args.r, 0)
        SendCommand(args.al, senderAddress, args.r, args.l)
        SendCommand(args.al | 0x40, senderAddress | 0x40, args.r, 0)
    if args.b != 0:
        SendCommand(args.al | 0x40, senderAddress | 0x40, args.r, 0)
        SendCommand(args.ab, senderAddress, args.r, args.b)
        SendCommand(args.ab | 0x40, senderAddress | 0x40, args.r, 0)
