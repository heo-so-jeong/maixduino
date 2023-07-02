from fpioa_manager import fm
from Maix import GPIO
import utime

def led_order(number):
    if number == 1:
        led_r.value(1)
    if number == 2:
        led_r.value(0)

io_led_blue = 15
fm.register(io_led_blue, fm.fpioa.GPIO0)

led_r = GPIO(GPIO.GPIO0, GPIO.OUT)
s = 'b'
while(True):
    led_r.value(1)
    if s != 'a':
        s = input()
    if s == 'a':
        for i in range(1,5):
            utime.sleep_ms(100)
            led_order(i)
            num = i
        for j in range(4,0,-1):
            utime.sleep_ms(100)
            led_order(j)
