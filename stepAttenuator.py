from AttenuatorDriver import AttenuatorDriver
import argparse
import time


def valid_commands(cmd):
    if cmd.lower() not in ['set', 'get', 'play']:
        msg = '%s is not a valid command' % cmd
        raise argparse.ArgumentTypeError(msg)
    return cmd.lower()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('commands', type=valid_commands, nargs='*',
                        default=['get'],
                        help='valid commands are: set, get and play.'
                        ' get is the default')
    parser.add_argument('-a', type=int, metavar='attenuation',
                        help='desired attentuation')

    args = parser.parse_args()
    # print(args)

    ad = AttenuatorDriver()
    for cmd in args.commands:
        if cmd == 'get':
            print('%d dB' % ad.getAttenuation())
        elif cmd == 'set':
            ad.setAttenuation(args.a)
            print('Setting attenuation to %d dB' % args.a)
        elif cmd == 'play':
            for a in [0, 40, 80, 100, 110, 114, 118, 120, 121, 0, 121, 0]:
                ad.setAttenuation(a)
                time.sleep(0.5)
            for r in [9, 10]:
                ad.closeRelay(r)
                time.sleep(1)
            for r in [9, 10]:
                ad.openRelay(r)
                time.sleep(1)
