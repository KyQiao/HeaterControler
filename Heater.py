#!/usr/bin/python3
import pigpio
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np


class Heater(object):
    """
    Hardware PWM is used
    using GPIO18 to control output
    using ADC channel 1 as input
    using GPIO13 and ADC channel 3 as reference
    """

    # setup initial temp and frequency for pwm
    def __init__(self, initTemp=25.0, frequency=9000):
        super(Heater, self).__init__()
        self.initTemp = initTemp
        self.frequency = frequency
        self.MaxTemp = 33.0
        self.pi = pigpio.pi()

        # 9000hz give a relative nice curve
        self.pi.hardware_PWM(13, self.frequency, 0)
        self.pi.hardware_PWM(18, self.frequency, 0)

        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        # Create single-ended input on channel 1
        self.chanRef = AnalogIn(ads, ADS.P1)
        self.chanCali = AnalogIn(ads, ADS.P3)

        self.readObejectiveTemp()
        self.setTemp(initTemp)

    # define exit behavior
    def __del__(self):
        # seems something here is wrong
        # self.pi.hardware_PWM(13, 0, 0)
        # self.pi.hardware_PWM(18, 0, 0)
        self.pi.stop()
        print("Heater exit success")
        print("!!! Unplug the socket !!!")

    def readObejectiveTemp(self):
        self.obejectiveTemp = self.chanRef.voltage*10

    def readCalibrationTemp(self):
        self.caliTemp = self.chanCali.voltage*10

    # set the temp on Heater within tolerance
    # I think 0.1 is a good choice
    def setTemp(self, targetTemp, tolerance=0.1):
        self.temp = targetTemp
        self.pi.hardware_PWM(18, self.frequency, int(
            targetTemp/self.MaxTemp*1000000))
        self.pi.hardware_PWM(13, self.frequency, int(
            targetTemp/self.MaxTemp*1000000))
        # remaining part is not implement

    def outputBanner(self):
        return("{} {} {}\n".format('Setpoint', 'Output', 'Objective'))

    def outputTemp(self):
        self.readObejectiveTemp()
        self.readCalibrationTemp()
        return("{:>5.2f}  {:>5.2f}  {:>5.2f} \n".format(
            self.temp, self.caliTemp, self.obejectiveTemp))


class TempCycle(Heater):
    """
    initTemp: start temp for heater
    finalTemp: end temp for heater
    cycleTime: cycle how many times. 1 cycle ~ 30min
    increase_rate: max rate measured is 0.3C/min,set to 0.2C/min by default
    decrease_rate: max rate measured is 1/6 C/min,set to 0.13 by default
    tempStep: step between temps
    outputStep: time between two lines, a loop is around 60s
    """

    def __init__(self, initTemp, finalTemp,
                 cycleNumber=20,
                 increase_rate=0.2, decrease_rate=0.10, tempStep=0.2,
                 outputStep=10):
        super(TempCycle, self).__init__(initTemp, frequency=9000)
        self.initTemp = initTemp
        self.finalTemp = finalTemp
        self.increase_rate = increase_rate
        self.decrease_rate = decrease_rate
        self.tempStep = tempStep
        self.cycleNumber = cycleNumber
        self.outputStep = outputStep
        if self.initTemp > self.finalTemp:
            self.increase = True
        else:
            self.increase = False

    # if increase, rate = increase_rate
    # else rate = decrease_rate
    def _rate_(self):
        return self.decrease_rate + int(self.increase) *\
            (self.increase_rate-self.decrease_rate)

    def start(self):
        filename = time.strftime(
            "%m-%d-at-%H:%M-year%YCyclelog.txt", time.localtime())
        with open(filename, 'w') as f:
            self.setTemp(self.initTemp)

            f.write(self.outputBanner())
            f.write("timestep={}s\n".format(self.outputStep))
            while self.cycleNumber:

                # from start to end
                # finaltemp is include in the next loop
                for setpoint in np.arange(self.initTemp, self.finalTemp, self.tempStep):
                    startTime = time.time()
                    self.setTemp(setpoint)
                    rate = self._rate_()
                    while time.time()-startTime < self.tempStep/rate*60:
                        f.write(self.outputTemp())
                        time.sleep(self.outputStep)
                    self.increase = False

                # from end to start
                # inittemp is include in the next loop
                for setpoint in np.arange(self.finalTemp, self.initTemp, -self.tempStep):
                    startTime = time.time()
                    self.setTemp(setpoint)
                    rate = self._rate_()
                    while time.time()-startTime < self.tempStep/rate*60:
                        f.write(self.outputTemp())
                        time.sleep(self.outputStep)
                    self.increase = False

                self.cycleNumber -= 1


class TempSchedule(Heater):
    """
    schedule: temp list for heater
    reside_time: time list for each temp.choose the longer one
                compared to calculated one.
    """

    def __init__(self, schedule, reside_time,
                 cycleNumber=20,
                 increase_rate=0.2, decrease_rate=0.10, tempStep=0.2,
                 outputStep=10):
        super(TempSchedule, self).__init__(initTemp=25, frequency=9000)
        self.schedule = schedule
        self.reside_time = reside_time
        self.increase_rate = increase_rate
        self.decrease_rate = decrease_rate
        self.tempStep = tempStep
        self.cycleNumber = cycleNumber
        self.outputStep = outputStep

    def prepare(self):
        self.tempLength = len(self.schedule)
        self.increaseList = [self.schedule[(i+1) % self.tempLength] - self.schedule[i]
                             for i in range(self.tempLength)]
        self.increaseRateList = [self.increase_rate if x > 0 else self.decrease_rate
                                 for x in self.increaseList]
        self.calculatedTime = [self.increaseList[i]/self.increaseRateList[i]
                               for i in range(self.tempLength)]
        for i in range(self.tempLength):
            if self.reside_time[i] < abs(self.calculatedTime[i]):
                self.reside_time[i] = abs(self.calculatedTime[i])

    def start(self):
        self.prepare()
        filename = time.strftime(
            "%m-%d-at-%H:%M-year%YCyclelog.txt", time.localtime())
        with open(filename, 'w') as f:
            f.write(self.outputBanner())
            f.write("timestep={}s\n".format(self.outputStep))
            while self.cycleNumber:
                for i in range(self.tempLength):
                    setpoint = self.schedule[i]
                    rate = self.increaseRateList[i]
                    staytime = self.reside_time[i]
                    startTime = time.time()
                    self.setTemp(setpoint)
                    while time.time()-startTime < staytime*60:
                        f.write(self.outputTemp())
                        time.sleep(self.outputStep)
                self.cycleNumber -= 1


if __name__ == '__main__':
    test = Heater(25.0)
    del test
    test = TempCycle(25, 26)
    del test
