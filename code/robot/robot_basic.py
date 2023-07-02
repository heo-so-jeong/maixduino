import sensor, image, lcd, time
from Maix import GPIO
from fpioa_manager import fm
from board import board_info
from machine import Timer,PWM
import utime
import gc, sys

lcd.init()

tim1 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
tim2 = Timer(Timer.TIMER0, Timer.CHANNEL1, mode=Timer.MODE_PWM)
tim3 = Timer(Timer.TIMER0, Timer.CHANNEL2, mode=Timer.MODE_PWM)
tim4 = Timer(Timer.TIMER0, Timer.CHANNEL3, mode=Timer.MODE_PWM)

ch1 = PWM(tim1, freq=256, duty=50, pin=24)
ch2 = PWM(tim2, freq=256, duty=50, pin=32)
ch3 = PWM(tim3, freq=256, duty=50, pin=13)
ch4 = PWM(tim4, freq=256, duty=50, pin=12)

duty = 0
ch1.duty(duty)
ch2.duty(duty)
ch3.duty(duty)
ch4.duty(duty)

fm.register(21, fm.fpioa.GPIOHS0)
btn = GPIO(GPIO.GPIOHS0, GPIO.IN ,GPIO.PULL_UP)

def straight():
    ch1.duty(0)
    ch2.duty(90)
    ch3.duty(90)
    ch4.duty(0)

def right_move():
    ch1.duty(0)
    ch2.duty(90)
    ch3.duty(0)
    ch4.duty(0)

def left_move():
    ch1.duty(0)
    ch2.duty(0)
    ch3.duty(90)
    ch4.duty(0)

def stop():
    ch1.duty(0)
    ch2.duty(0)
    ch3.duty(0)
    ch4.duty(0)

sensor_window=(224, 224)
lcd_rotation=0
sensor_hmirror=False
sensor_vflip=False

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing(sensor_window)
sensor.set_hmirror(sensor_hmirror)
sensor.set_vflip(sensor_vflip)
sensor.run(1)

lcd.init(type=1)
lcd.rotation(lcd_rotation)
lcd.clear(lcd.WHITE)

try:
    img = sensor.snapshot()
    lcd.display(img)
except Exception:
    img = image.Image(size=(320, 240))
    lcd.display(img)

state_previous = 1
count = 0
try:
    while(True):
        img = sensor.snapshot()
        state_current = btn.value()
        if state_current == 0:
            if state_previous == 1:
                count = count + 1
                state_previous = 0
                stop()
                img.clear()
                img.draw_string(100,100,"END", color=(255, 0, 0),scale=4)
                lcd.display(img)
                break
            utime.sleep_ms(100)

        left_move()
        lcd.display(img)

except Exception as e:
    sys.print_exception(e)
