#!/usr/bin/python3
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn



# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# Create single-ended input on channel 1
chanRef = AnalogIn(ads, ADS.P1)
chanCali = AnalogIn(ads, ADS.P3)


def outputBanner():
    print("{} {}".format('Output', 'Objective'))

def outputTemp():
    print("{:>5.2f}  {:>5.2f}".format(chanCali.voltage*10, chanRef.voltage*10))


if __name__ == '__main__':
    outputBanner()
    while True:
        outputTemp()
        time.sleep(20)
