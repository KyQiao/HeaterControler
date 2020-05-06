#!/usr/bin/python3
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# Create single-ended input on channel 1
chanRef = AnalogIn(ads, ADS.P1)
chanCali = AnalogIn(ads, ADS.P3)


def outputBanner():
    print("{} {} {}".format('Time', 'ObjectiveTemp', 'Variance'))


def outputTemp(Mean, Variance):
    print(time.strftime("%H:%M:%S", time.localtime()) +
          "  {:>5.2f} {:>4.3f}".format(Mean, Variance))


if __name__ == '__main__':
    outputTimeStep = 1
    screenOutput = False

    filename = time.strftime(
        "%m-%d-at-%H:%M-year%YRecordLog.txt", time.localtime())
    with open(filename, 'w') as f:
        if screenOutput:
            outputBanner()
        f.write("{} {} {}\n".format('Time', 'ObjectiveTemp', 'Variance'))
        while True:
            startTime = time.time()
            tempList = []
            while time.time()-startTime < outputTimeStep:
                tempList.append(chanRef.voltage*10)
                time.sleep(outputTimeStep//50)
            tempArray = np.array(tempList)
            Mean, Var = np.mean(tempArray), np.var(tempArray)
            f.write(time.strftime("%H:%M:%S", time.localtime()) +
                    "  {:>5.2f} {:>4.3f}\n".format(Mean,Var))
            if screenOutput:
                outputTemp(Mean, Var)
