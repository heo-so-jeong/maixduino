from machine import Timer,PWM
import random
import time, network
from Maix import GPIO
from fpioa_manager import fm

class wifi():
    # IO map for ESP32 on Maixduino
    fm.register(25,fm.fpioa.GPIOHS10)#cs
    fm.register(8,fm.fpioa.GPIOHS11)#rst
    fm.register(9,fm.fpioa.GPIOHS12)#rdy
    print("Use Hareware SPI for other maixduino")
    fm.register(28,fm.fpioa.SPI1_D0, force=True)#mosi
    fm.register(26,fm.fpioa.SPI1_D1, force=True)#miso
    fm.register(27,fm.fpioa.SPI1_SCLK, force=True)#sclk
    nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10, rst=fm.fpioa.GPIOHS11, rdy=fm.fpioa.GPIOHS12, spi=1)

print("ESP32_SPI firmware version:", wifi.nic.version())

tim1 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
tim2 = Timer(Timer.TIMER0, Timer.CHANNEL1, mode=Timer.MODE_PWM)
tim3 = Timer(Timer.TIMER0, Timer.CHANNEL2, mode=Timer.MODE_PWM)

ch1 = PWM(tim1, freq=500000, duty=50, pin=21)
ch2 = PWM(tim2, freq=500000, duty=50, pin=22)
ch3 = PWM(tim3, freq=500000, duty=50, pin=23)
duty=0
dir = True
while True:
    try:
        # get ADC0~5
        adc = wifi.nic.adc((0,))
    except Exception as e:
        print(e)
        continue
    duty = adc[0]/4096*100
    ch1.duty(duty)
    ch2.duty(duty)
    ch3.duty(duty)
