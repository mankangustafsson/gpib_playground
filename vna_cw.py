from args_validate import add_frequency
from Devices import Device
from Lab import Lab

from quantiphy import Quantity
import argparse


def valid_port(p):
    if p == "1":
        return "S11"
    elif p == "2":
        return "S22"
    raise argparse.ArgumentTypeError(f"{p} is not a valid port")


def valid_power(p):
    try:
        pf = float(p)
        power = Quantity(pf, "dB")
        if power < -75.0 or power > -5.0:
            raise argparse.ArgumentTypeError(f"{power} is outside valid range")
        return power
    except argparse.ArgumentTypeError:
        raise
    except ValueError:
        raise argparse.ArgumentTypeError(f"{p}%s is not a power")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_frequency(parser)
    parser.add_argument(
        "-p", type=valid_port, metavar="port", default="1", help="desired output port"
    )
    parser.add_argument(
        "-d",
        type=valid_power,
        metavar="power",
        default="-10.0",
        help="desired output power in dBm",
    )
    parser.add_argument("-u", metavar="unit", default="8722", help="unit to connect to")
    parser.add_argument(
        "-v", action="store_true", default=False, help="enable verbose output"
    )
    args = parser.parse_args()
    if args.v:
        print(args)

    dev = Lab.connectByType(Device.Type.VNA, hint=args.u, verbose=args.v)
    if dev is None:
        exit(1)

    q = f"{args.p}; POWE {args.d}; CWFREQ {args.f}"
    if args.v:
        print(q)
    dev.write(q)
    dev.close()
