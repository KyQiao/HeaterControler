#!/usr/bin/python3
# generate data for plot

import RPi.GPIO as io
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np


def main():
    try:
        io.setmode(io.BCM)
        io.setup(12, io.OUT)
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        chan = AnalogIn(ads, ADS.P3)
        my_pwm = io.PWM(12, 100)
        my_pwm.start(1)
        for frequency in [100, 200, 300, 400, 500, 600, 700, 800, 900,1000]:
            my_pwm.ChangeDutyCycle(1)
            my_pwm.ChangeFrequency(frequency)
            with open("SoftwareAvgDataF"+str(frequency)+".txt", 'w') as f:
                f.write("# pwm     avgADC    varADC \n")
                for temp in range(1, 101):
                    my_pwm.ChangeDutyCycle(temp)
                    startTime = time.time()
                    tmp = []
                    while time.time()-startTime < 10:
                        tmp.append(chan.voltage)
                        time.sleep(0.1)
                    tmp = np.array(tmp)
                    f.write("{:>5.3f}\t{:>5.3f}\t{:>5.3f}\n".format(
                        temp/100*3.3, np.mean(tmp), np.var(tmp)))
                    print("finish "+str(temp)+"%")
    except (KeyboardInterrupt, SystemExit):
        print("Keyboard Interrupt")
    finally:
        my_pwm.stop()
        io.cleanup()


if __name__ == '__main__':
    main()
