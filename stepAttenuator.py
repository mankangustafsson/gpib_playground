from AttenuatorDriver import AttenuatorDriver
import argparse


def valid_commands(cmd):
    if cmd.lower() not in ['set', 'get']:
        msg = '%s is not a valid command' % cmd
        raise argparse.ArgumentTypeError(msg)
    return cmd.lower()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('commands', type=valid_commands, nargs='*',
                        default=['get'],
                        help='valid commands are: set and get.'
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
