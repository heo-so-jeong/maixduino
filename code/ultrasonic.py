from fpioa_manager import fm
from Maix import GPIO
import utime
from machine import Timer

count = 0

def on_timer(timer):
    global count
    count = count + 1 # 1 20us

def test_irq(pin_num):
    global count
    tim.stop()
    if count > 10:
        distance =((340*count)/1000)/2
        print(distance)
    count = 0

def ultra_send():
    for _ in range(1):
        trig.value(1)
        utime.sleep_us(10)
        trig.value(0)
        utime.sleep_us(10)
    tim.start()

io_echo_pin = 14
io_trig_pin = 13
fm.register(io_echo_pin, fm.fpioa.GPIOHS0) # GPIO HS(High Speed) 0
fm.register(io_trig_pin, fm.fpioa.GPIO0)

tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=20, unit=Timer.UNIT_US, callback=on_timer, arg=on_timer)

echo = GPIO(GPIO.GPIOHS0, GPIO.IN)
trig = GPIO(GPIO.GPIO0, GPIO.OUT)
echo.irq(test_irq, GPIO.IRQ_FALLING, GPIO.WAKEUP_NOT_SUPPORT,10) # interrupt 방해하다.

while True: #while 부정확하다. ? 디바이스가 여유가 될때마다 실행한다. 즉 메인 while문으로는 시간을 측정할 수가 없다.
    ultra_send()
    utime.sleep(1)
