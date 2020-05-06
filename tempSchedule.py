#!/usr/bin/python3
from Heater import TempSchedule


def main():
    # high temp short cycle
    # schedule = [28.5, 28.7, 28.9, 29.1, 29.3, 29.5, 29.3, 29.1, 28.9, 28.7]
    # reside_time = [1, 1, 1, 3, 5, 10, 5, 3, 1, 1]
    schedule = [27, 27.2, 27.4, 27.6, 27.8, 28., 28.2, 28.4, 28.6, 28.8, 29, 29.2, 29.4, 29.6,
                29.4, 29.2, 29., 28.8, 28.6, 28.4, 28.2, 28., 27.8, 27.6, 27.4, 27.2]

    reside_time =[10, 5, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 5, 20,
                5, 3, 2, 2, 2, 2, 2, 2, 2, 2,3, 5]
    # 1 h per cycle
    h = TempSchedule(schedule, reside_time, cycleNumber=50)
    try:
        h.start()
    finally:
        del h


if __name__ == '__main__':
    main()
