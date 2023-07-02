from fpioa_manager import fm
from machine import Timer,PWM
import utime
from Maix import GPIO

io_btn = 24

tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch = PWM(tim, freq=261, duty=50, pin=22)
fm.register(io_btn, fm.fpioa.GPIO0)
btn = GPIO(GPIO.GPIO0, GPIO.IN, GPIO.PULL_UP)

um =  [261,293,329,349,391,440,493]

while True:
    if btn.value() == 0:
        ch.duty(50)
        for i in um:
            ch.freq(i)
            utime.sleep_ms(500)
    else:
        ch.duty(0)



