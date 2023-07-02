from fpioa_manager import fm
from Maix import GPIO
import utime

io_btn = 22
fm.register(io_btn, fm.fpioa.GPIO1)

btn = GPIO(GPIO.GPIO1, GPIO.IN)

while(True):
    btn_state = btn.value()
    print(btn_state)
