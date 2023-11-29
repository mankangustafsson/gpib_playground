from enum import Enum, auto
from quantiphy import Quantity


class Standard:
    class Type(Enum):
        SHORT = auto(),
        OPEN = auto(),
        LOAD = auto(),
        THRU = auto()

        def __str__(self):
            return self.name.lower()

    class Sex(Enum):
        MALE = auto(),
        FEMALE = auto()

        def __str__(self):
            return self.name.lower()

    def __init__(self, s_type, sex, cmds, name=None):
        self.name = name
        self.s_type = s_type
        self.sex = sex
        self.cmds = cmds

    def get_delay(self):
        for c in self.cmds:
            s = c.split(' ', 1)
            if s[0] == 'OFSD':
                return Quantity(s[1], 's')
        return Quantity(0.0, 's')

    def __str__(self):
        name = '' if self.name is None else f'{self.name:10} '
        return f'{name}{self.s_type:5} {self.sex:6} delay: {self.get_delay():8}'

    def load(self, dev):
        name = '' if self.name is None else f' ({self.name}'
        print(f'{self.s_type} {self.sex}{name}...', end='', flush=True)
        for cmd in self.cmds:
            dev.write(cmd)
        if self.s_type == Standard.Type.LOAD:
            dev.write('OFSL 0.0E+9')
            dev.write('C0 0.0')
            dev.write('C1 0.0')
            dev.write('C2 0.0')
            dev.write('C3 0.0')


class CalKit:
    def __init__(self, name, short_name, max_freq, standards):
        self.name = name
        self.short_name = short_name
        self.max_freq = max_freq
        self.standards = standards

    def get_standard(self, s_type, sex):
        for s in self.standards:
            if s.s_type == s_type and s.sex == sex:
                return s
        return None

    def __str__(self):
        fs = Quantity(self.max_freq, 'Hz')
        return f'{self.name} {fs}'

    def __load_standard(self, dev, s_type, sex=None):
        s = self.get_standard(s_type, sex)
        if s is None and s_type != Standard.Type.THRU:
            return
        if s:
            s.load(dev)
        else:  # s_type == Standard.Type.THRU:
            print('No delay thru ...', end='', flush=True)
            dev.write('DEFS 4')
            dev.write('STDTDELA')
            dev.write('OFSZ 50')
            dev.write('OFSD 0.0E-12')
            dev.write('OFSL 0.0E+9')
        dev.write('MINF 0')
        dev.write(f'MAXF {self.max_freq}')
        dev.write('STDD')
        print('done')

    def print_kit(self):
        header = f'{self}'
        print(header)
        line = "-" * len(header)
        print(line)
        for s in self.standards:
            print(s)
        print(line)

    def load(self, dev, genders):
        print(f'Loading {self} {genders} '
              'cal kit to VNA...', flush=True)
        dev.write('CALKN50')  # To get the class definitions like we want
        dev.write('MODI1')

        self.__load_standard(dev, Standard.Type.SHORT, Standard.Sex.MALE)
        self.__load_standard(dev, Standard.Type.OPEN, Standard.Sex.MALE)
        if genders in ['MM', 'M0']:
            self.__load_standard(dev, Standard.Type.LOAD, Standard.Sex.MALE)
        else:  # 'FF' & 'F0'
            self.__load_standard(dev, Standard.Type.LOAD, Standard.Sex.FEMALE)

        if genders == 'MM':
            self.__load_standard(dev, Standard.Type.THRU, Standard.Sex.MALE)
        elif genders == 'FF':
            self.__load_standard(dev, Standard.Type.THRU, Standard.Sex.FEMALE)
        else:
            self.__load_standard(dev, Standard.Type.THRU)

        self.__load_standard(dev, Standard.Type.SHORT, Standard.Sex.FEMALE)
        self.__load_standard(dev, Standard.Type.OPEN, Standard.Sex.FEMALE)

        kitname = f'{self.short_name} ({genders})'
        dev.write(f'LABK "{kitname}"')
        dev.write('KITD')
        dev.write('OPC?; SAVEUSEK; SOFR')
        print(f'{self.name} cal kit loaded as {kitname}')


# SMA Rosenberger parts 6GHz
sma_6ghz = CalKit(name='Rosenberger SMA', short_name='SMA', max_freq='6E+9',
                  standards=[Standard(Standard.Type.SHORT, Standard.Sex.MALE,
                                      ['DEFS 1',
                                       'STDTSHOR',
                                       'OFSZ 50',
                                       'OFSD 26.296763E-12',
                                       'OFSL 0.0E+9',
                                       'C0 1.972678',
                                       'C1 6613.309399',
                                       'C2 -1625.587777',
                                       'C3 94.519818']),
                             Standard(Standard.Type.OPEN, Standard.Sex.MALE,
                                      ['DEFS 2',
                                       'STDTOPEN',
                                       'OFSZ 50',
                                       'OFSD 43.059930E-12',
                                       'OFSL 1.818363E+9',
                                       'C0 -14.992043',
                                       'C1 -1009.382660',
                                       'C2 1377.725656',
                                       'C3 -138.223997']),
                             Standard(Standard.Type.LOAD, Standard.Sex.MALE,
                                      ['DEFS 3',
                                       'LABS "LOAD"',
                                       'STDTLOAD',
                                       'OFSZ 52.383099',
                                       'OFSD 17.961624E-12']),
                             Standard(Standard.Type.LOAD, Standard.Sex.FEMALE,
                                      ['DEFS 3',
                                       'LABS "LOAD"',
                                       'STDTLOAD',
                                       'OFSZ 50.589652',
                                       'OFSD 29.614480E-12']),
                             Standard(Standard.Type.THRU, Standard.Sex.MALE,
                                      ['DEFS 4',
                                       'STDTDELA',
                                       'OFSZ 50.747533',
                                       'OFSD 42.264620E-12']),
                             Standard(Standard.Type.THRU, Standard.Sex.FEMALE,
                                      ['DEFS 4',
                                       'STDTDELA',
                                       'OFSZ 50',
                                       'OFSD 76.991933E-12']),
                             Standard(Standard.Type.SHORT, Standard.Sex.FEMALE,
                                      ['DEFS 7',
                                       'STDTSHOR',
                                       'OFSZ 50',
                                       'OFSD 0.0E-12',
                                       'OFSL 962.266512E+9',
                                       'C0 28.454226',
                                       'C1 2380.746494',
                                       'C2 -3135.518359',
                                       'C3 358.471292']),
                             Standard(Standard.Type.OPEN, Standard.Sex.FEMALE,
                                      ['DEFS 8',
                                       'STDTOPEN',
                                       'OFSZ 50',
                                       'OFSD 0.0E-12',
                                       'OFSL 0.0E+9',
                                       'C0 0',
                                       'C1 0',
                                       'C2 0',
                                       'C3 0'])])
