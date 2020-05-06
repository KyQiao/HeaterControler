#!/usr/bin/python3
from Heater import TempCycle


def main():
    initTemp = 27
    finalTemp = 29.5
    # 1 h per cycle
    h = TempCycle(initTemp,finalTemp,cycleNumber=30)
    try:
        h.start()
    finally:
        del h

if __name__ == '__main__':
    main()