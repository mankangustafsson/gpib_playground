from quantiphy import Quantity


class Probe:
    def __init__(self, name, ref_cf, cal_read, cf_table):
        self.name = name
        self.ref_cf = ref_cf
        self.cal_read = cal_read
        self.cf_table = cf_table

    def __str__(self):
        return 'Name: %s Ref CF: %5.1f%%' % (self.name, self.ref_cf)

    def get_cf(self, frequency):
        prev_f = None
        prev_cf = None
        if frequency is None:
            frequency = 1.0
        for f, cf in self.cf_table.items():
            if frequency == f:
                return cf
            if frequency < f and prev_f is None:
                print('Frequency %s is lower than probe %s lowest frequency %s'
                      % (str(Quantity(frequency, 'Hz')),
                         self.name, str(Quantity(f, 'Hz'))))
                return cf
            if frequency > f:
                prev_f = f
                prev_cf = cf
            else:
                a = (cf - prev_cf) / (f - prev_f)
                b = cf - f * a
                return frequency * a + b
        print('Frequency %s is higher than probe %s highest frequency %s'
              % (str(Quantity(frequency, 'Hz')),
                 self.name, str(Quantity(f, 'Hz'))))
        return prev_cf

    def print_cal_table(self):
        print('\nCalibration table')
        print('-----------------')
        for f, cf in self.cf_table.items():
            print('{:9q} {:7q}'.format(Quantity(f, 'Hz'), Quantity(cf, '%')))
        print('-----------------\n')
