import pyvisa
import time
import numpy as np

class DMM:

    rm = None
    device_instance = None

    """
    Class constructor
    """
    def __init__(self):
        self.rm = pyvisa.ResourceManager()

    """
    :return list of visa devices connected
    """
    def device_list(self):
        return self.rm.list_resources()

    """
    Method connecting to Visa device at given address
    :arg address: visa device address
    :return True if device found, None if device not found
    """
    def connect(self, address):
        try:
            self.device_instance = self.rm.open_resource(address)
            return True
        except pyvisa.VisaIOError as err:
            print(str(err))
            return None

    """
    :return device identificator
    """
    def identificator(self):
        return self.device_instance.query('*IDN?')

    """
    :return 0 if device pass self test; 1 if device fail
    """
    def selftest(self):
        return self.device_instance.query('TEST:ALL?')

    """
    Method clear data
    """
    def clear_data(self):
        return self.device_instance.query('CALC:CLE:IMM')

    """
    :return Resistance value using 2 wire method
    """
    def measure_resistance_2wire(self):
        return self.device_instance.query(':MEASure:RESistance? AUTO,DEFault')

    """
    :return Resistance value using 4 wire method
    """
    def measure_resistance_4wire(self):
        return self.device_instance.query(':MEASure:FRESistance? AUTO,DEFault')

    """
    :return DC voltage value
    """
    def measure_voltage_dc(self):
        return self.device_instance.query(':MEASure:VOLT:DC? AUTO,DEFault')


    """
    Method perform 10 measurments of resistance and using numpy calculate average and standard deviation
    :return average, standard deviation
    """
    def calculate_average_RES_2wire(self):
        self.device_instance.write('CONF:RES AUTO,DEF')
        time.sleep(0.1)
        self.device_instance.write('SAMP:COUN 10')
        time.sleep(0.1)
        meas_str = self.device_instance.query('READ?', delay=5)
        time.sleep(0.1)
        meas_list = str(meas_str).split(',')
        meas_floats = []
        for measure in meas_list:
            measure = float(measure)
            meas_floats.append(measure)

        #print(meas_floats)
        average = np.average(meas_floats)
        stddev = np.std(meas_floats)

        return average, stddev

    #TODO: zrobic srednio dla pomiaru wszustkich mierzonych wartosci, dodac pomiary innych wartosci

if __name__=="__main__":
    print('DMM class. Start Test')

    dmm = DMM()

    print(dmm.device_list())
    connection_successful = dmm.connect('TCPIP0::K-34461A-09586.local::hislip0::INSTR')

    if not connection_successful:
        exit()

    print(dmm.identificator())
    print(dmm.measure_resistance_2wire())
    print(dmm.measure_voltage_dc())

    average, standard_dev = dmm.calculate_average_RES_2wire()
    tolerance = standard_dev *3
    print(f'{average} +/- {tolerance}')
    #print(dmm.selftest())
