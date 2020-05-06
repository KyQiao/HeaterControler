# Heater Controller
 Using Raspberry Pi to control objective heater



## prerequisites

### Hardware

- Raspberry Pi: Any model should be fine. Early model need to change some parameter in code. 
- Dupont thread, female to male and female to female.
- ADC chip.
- Objective Heater

### Software

- `pigpio`
- `adafruit_ads1x15`
- `numpy`

In a nutshell, you need driver for the ADC chip and  hardware level GPIO port driver `pigpio`. If you use `NOOBS` system for raspberry Pi, installation will be easy.

## Usage

Refer my [blog](https://kyqiao.github.io/DocumentationRepo/2020/04/24/RaspberryPi/) for info.

A briefing about usage:

#### Print heater's objective temperature:

```
python3 measureOutput.py
//or chomd +x for file
./measureOutput.py
```

#### Linearly cycle the temperature:

```
python3 tempCycle.py
```

The file is self-explain.

After running, a log file will be produced. You can `./log/LogPlot.py` to vis the log. Just change the file name in python file.

#### Customized temperature control

```
python3 tempSchedule.py
```

Schedule is the temp you set and reside_time is the time set for corresponding temperature. It will cycle from start of the list after schedule is finished.

Also it will produce a log file.

#### Record the temperature only

```bash
python3 tempRecorder.py
```

Self-explain file.