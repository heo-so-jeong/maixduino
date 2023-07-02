from fpioa_manager import fm
from Maix import GPIO
import utime

io_btn = 22
fm.register(io_btn, fm.fpioa.GPIO1)

btn = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_DOWN)
count = 0
while(True):
    state_current = btn.value()
    if state_current == 1:
        if state_previous == 0 :
            count = count + 1
            state_previous = 1
            print(count)
        utime.sleep_ms(100)
    else :
        state_previous = 0


