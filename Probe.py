from quantiphy import Quantity

class Probe:
    def __init__(self, name, ref_cf, cal_read, cf_table):
        self.name = name
        self.ref_cf = ref_cf
        self.cal_read = cal_read
        self.cf_table = cf_table
        
    def __str__(self):
        return 'Name: %s Ref CF: %5.1f%%' %(self.name, self.ref_cf)
    
    def get_cf(self, frequency):
        last_f = None
        last_cf = None
        for f, cf in self.cf_table.items():
            if frequency == f:
                return cf
            if frequency < f and last_f is None:
                print('Frequency %s is lower than probe %s lowest frequency %s'
                      %(str(Quantity(frequency, 'Hz')),
                        self.name, str(Quantity(f, 'Hz'))))
                return cf
            if frequency > f:
                last_f = f
                last_cf = cf
            else:
                a = (cf - last_cf) / (f - last_f)
                b = cf - f * a
                return frequency * a + b
        print('Frequency %s is higher than probe %s highest frequency %s'
              %(str(Quantity(frequency, 'Hz')),
                self.name, str(Quantity(f, 'Hz'))))
        return last_cf

probes = [Probe('8481A', 100.0, 0.0, dict([( 0.01E+9, 98.2), # HP E4436B/8482A
                                           ( 0.03E+9, 99.5), # HP E4436B/8482A
                                           ( 0.1E+9, 98.9),
                                           ( 0.3E+9, 98.5),  # HP E4436B/8482A
                                           ( 1.0E+9, 97.2),  # HP E4436B/8482A 
                                           ( 1.5E+9, 97.0),  # HP E4436B/8482A
                                           ( 2.0E+9, 99.2),
                                           ( 3.0E+9, 98.5),
                                           ( 4.0E+9, 98.1),
                                           ( 5.0E+9, 96.4),
                                           ( 6.0E+9, 96.0),
                                           ( 7.0E+9, 97.2),
                                           ( 8.0E+9, 95.5),
                                           ( 9.0E+9, 94.5),
                                           (10.0E+9, 92.8),
                                           (11.0E+9, 93.3),
                                           (12.4E+9, 93.2),
                                           (13.0E+9, 92.2),
                                           (14.0E+9, 92.5),
                                           (15.0E+9, 91.4),
                                           (16.0E+9, 92.5),
                                           (17.0E+9, 94.3),
                                           (18.0E+9, 93.5)])),
          Probe('8482A', 98.0, 0.0, dict([(   0.1E+6, 96.7),
                                          (   0.3E+6, 97.9),
                                          (   1.0E+6, 99.3),
                                          (   3.0E+6, 98.9),
                                          (  10.0E+6, 98.3),
                                          (  30.0E+6, 98.4),
                                          ( 100.0E+6, 98.1),
                                          ( 300.0E+6, 97.6),
                                          (1000.0E+6, 97.3),
                                          (2000.0E+6, 96.2),
                                          (3000.0E+6, 90.3),
                                          (4000.0E+6, 89.5),    
                                          (4200.0E+6, 88.2),    
                                          (5000.0E+6, 82.4),    # HP8753D
                                          (5400.0E+6, 77.4),    # HP8753D
                                          (6000.0E+6, 77.0)])), # HP8753D
          Probe('8482Auc', 96.1, 0.0, dict([(   0.1E+6, 94.7),  # HP8753D/Probe 2
                                            (   0.3E+6, 95.6),    # HP8753D/Probe 2
                                            (   1.0E+6, 96.0),    # HP8753D/Probe 2
                                            (   3.0E+6, 96.0),    # HP8753D/Probe 2
                                            (  10.0E+6, 95.1),    # HP8753D/Probe 2
                                            (  30.0E+6, 96.2),    # HP8753D/Probe 2
                                            ( 100.0E+6, 95.8),    # HP8753D/Probe 2
                                            ( 300.0E+6, 96.3),    # HP8753D/Probe 2
                                            ( 500.0E+6, 96.8),    # HP8753D/Probe 2
                                            (1000.0E+6, 97.0),    # HP8753D/Probe 2
                                            (1500.0E+6, 93.6),    # HP8753D/Probe 2
                                            (2000.0E+6, 91.0),    # HP8753D/Probe 2
                                            (2600.0E+6, 98.0),    # HP8753D/Probe 2
                                            (3000.0E+6, 96.9),    # HP8753D/Probe 2
                                            (4000.0E+6, 79.2),    # HP8753D/Probe 2
                                            (4200.0E+6, 80.3),    # HP8753D/Probe 2
                                            (5000.0E+6, 97.8),    # HP8753D/Probe 2
                                            (5400.0E+6, 89.4),    # HP8753D/Probe 2
                                            (6000.0E+6, 75.2)])), # HP8753D/Probe 2
          Probe('8484A', 90.6, -30.0, dict([( 0.1E+9, 89.1),  
                                            ( 0.3E+9, 89.9),    
                                            ( 0.5E+9, 90.3),    
                                            ( 1.0E+9, 90.2),    
                                            ( 2.0E+9, 89.9),    
                                            ( 3.0E+9, 87.4),    
                                            ( 4.0E+9, 89.9),    
                                            ( 5.0E+9, 89.3),    
                                            ( 6.0E+9, 87.9),    
                                            ( 7.0E+9, 87.6),    
                                            ( 8.0E+9, 88.1),    
                                            ( 9.0E+9, 88.7),    
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
