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
        name = '' if self.name is None else f'{self.name:7} '
        return f'{name}{self.s_type:5} {self.sex:6} delay: {self.get_delay():9}'

    def load(self, dev):
        print(f'{self} ...', end='', flush=True)
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
        return f'{self.name} {self.short_name} {fs}'

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
        header = f'\n{self}'
        print(header)
        line = "-" * (len(header) + 11)
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

    def verify(self):
        stds = set()
        for std in self.standards:
            stds.add(f'{std.s_type}{std.sex}')
        return len(self.standards) == len(stds)
