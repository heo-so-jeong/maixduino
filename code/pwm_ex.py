from machine import Timer,PWM
import time
import random

tim1 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
tim2 = Timer(Timer.TIMER0, Timer.CHANNEL1, mode=Timer.MODE_PWM)
tim3 = Timer(Timer.TIMER0, Timer.CHANNEL2, mode=Timer.MODE_PWM)

ch1 = PWM(tim1, freq=500000, duty=50, pin=21)
ch2 = PWM(tim2, freq=500000, duty=50, pin=22)
ch3 = PWM(tim3, freq=500000, duty=50, pin=23)
duty=0
dir = True
while True:
    if dir:
        duty += 2
    else:
        duty -= 2
    if duty>100:
        duty = 100
        dir = False
    elif duty<0:
        duty = 0
        dir = True
    time.sleep_ms(50)
    ch1.duty(duty)
    ch2.duty(duty)
    ch3.duty(duty)

