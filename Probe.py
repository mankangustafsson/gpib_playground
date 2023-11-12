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
        

probes = [Probe('8481A', 100.0, 0.0, dict([(00.01E+9, 98.2),  # HP E4436B/8482A
                                           (00.03E+9, 99.5),  # HP E4436B/8482A
                                           (00.1E+9, 98.9),
                                           (00.3E+9, 98.5),   # HP E4436B/8482A
                                           (01.0E+9, 97.2),   # HP E4436B/8482A
                                           (01.5E+9, 97.0),   # HP E4436B/8482A
                                           (02.0E+9, 99.2),
                                           (03.0E+9, 98.5),
                                           (04.0E+9, 98.1),
                                           (05.0E+9, 96.4),
                                           (06.0E+9, 96.0),
                                           (07.0E+9, 97.2),
                                           (08.0E+9, 95.5),
                                           (09.0E+9, 94.5),
                                           (10.0E+9, 92.8),
                                           (11.0E+9, 93.3),
                                           (12.4E+9, 93.2),
                                           (13.0E+9, 92.2),
                                           (14.0E+9, 92.5),
                                           (15.0E+9, 91.4),
                                           (16.0E+9, 92.5),
                                           (17.0E+9, 94.3),
                                           (18.0E+9, 93.5)])),
          Probe('8482A', 98.0, 0.0, dict([(0000.1E+6, 96.7),
                                          (0000.3E+6, 97.9),
                                          (0001.0E+6, 99.3),
                                          (0003.0E+6, 98.9),
                                          (0010.0E+6, 98.3),
                                          (0030.0E+6, 98.4),
                                          (0100.0E+6, 98.1),
                                          (0300.0E+6, 97.6),
                                          (1000.0E+6, 97.3),
                                          (2000.0E+6, 96.2),
                                          (3000.0E+6, 90.3),
                                          (4000.0E+6, 89.5),
                                          (4200.0E+6, 88.2),
                                          (5000.0E+6, 82.4),     # HP8753D
                                          (5400.0E+6, 77.4),     # HP8753D
                                          (6000.0E+6, 77.0)])),  # HP8753D
          Probe('8482Auc', 96.1, 0.0,
                dict([(0000.1E+6, 94.7),     # HP8753D/Probe 2
                      (0000.3E+6, 95.6),     # HP8753D/Probe 2
                      (0001.0E+6, 96.0),     # HP8753D/Probe 2
                      (0003.0E+6, 96.0),     # HP8753D/Probe 2
                      (0010.0E+6, 95.1),     # HP8753D/Probe 2
                      (0030.0E+6, 96.2),     # HP8753D/Probe 2
                      (0100.0E+6, 95.8),     # HP8753D/Probe 2
                      (0300.0E+6, 96.3),     # HP8753D/Probe 2
                      (0500.0E+6, 96.8),     # HP8753D/Probe 2
                      (1000.0E+6, 97.0),     # HP8753D/Probe 2
                      (1500.0E+6, 93.6),     # HP8753D/Probe 2
                      (2000.0E+6, 91.0),     # HP8753D/Probe 2
                      (2600.0E+6, 98.0),     # HP8753D/Probe 2
                      (3000.0E+6, 96.9),     # HP8753D/Probe 2
                      (4000.0E+6, 79.2),     # HP8753D/Probe 2
                      (4200.0E+6, 80.3),     # HP8753D/Probe 2
                      (5000.0E+6, 97.8),     # HP8753D/Probe 2
                      (5400.0E+6, 89.4),     # HP8753D/Probe 2
                      (6000.0E+6, 75.2)])),  # HP8753D/Probe 2
          Probe('8484A', 90.6, -30.0, dict([(00.1E+9, 89.1),
                                            (00.3E+9, 89.9),
                                            (00.5E+9, 90.3),
                                            (01.0E+9, 90.2),
                                            (02.0E+9, 89.9),
                                            (03.0E+9, 87.4),
                                            (04.0E+9, 89.9),
                                            (05.0E+9, 89.3),
                                            (06.0E+9, 87.9),
                                            (07.0E+9, 87.6),
                                            (08.0E+9, 88.1),
                                            (09.0E+9, 88.7),
                                            (10.0E+9, 88.9),
                                            (11.0E+9, 87.8),
                                            (12.0E+9, 89.5),
                                            (12.4E+9, 91.0),
                                            (13.0E+9, 90.1),
                                            (14.0E+9, 94.5),
                                            (15.0E+9, 93.6),
                                            (16.0E+9, 97.0),
                                            (17.0E+9, 98.4),
                                            (18.0E+9, 100)])),
          ]
