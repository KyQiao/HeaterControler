#!/usr/bin/python3
# generate data for plot

import pigpio
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


def main():
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        chan = AnalogIn(ads, ADS.P3)
        pi = pigpio.pi()
        pi.hardware_PWM(13, 0, 0)
        for frequency in [10000, 20000, 30000, 40000, 50000,
                          60000, 70000, 80000, 90000, 100000]:
            pi.hardware_PWM(13, frequency, 10000)
            with open("HardwareAvgDataF"+str(frequency)+".txt", 'w') as f:
                f.write("# pwm     avgADC    varADC \n")
                for temp in range(1, 101):
                    pi.hardware_PWM(13, frequency,temp*10000)
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
        pi.hardware_PWM(13, 0, 0)
        pi.stop()


if __name__ == '__main__':
    main()
