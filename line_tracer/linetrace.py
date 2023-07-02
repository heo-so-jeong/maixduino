import sensor, image, lcd, time
from Maix import GPIO
from fpioa_manager import fm
from board import board_info
from machine import Timer,PWM
import gc, sys



lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(time = 2000)

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

min_degree = 70
max_degree = 110

tim = time.ticks_ms()

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
        state_current = btn.value()
        if state_current == 0:
           if state_previous == 1:
               count = count + 1
               state_previous = 0
               ch1.duty(0)
               ch2.duty(0)
               ch3.duty(0)
               ch4.duty(0)
               img.clear()
               img.draw_string(100,100,"END", color=(255, 0, 0),scale=4)
               lcd.display(img)
               break
#       theta 70보다 작고 110보다 크게 x1,2 160 기준 좌측
        img = sensor.snapshot()
        for l in img.find_lines(threshold = 2000, theta_margin = 25, rho_margin = 25):
            if (l.theta() <= min_degree) or (max_degree <= l.theta()):
                img.draw_line(l.line(), color = (255, 0, 0),scale=5)
                print((l.x1()+l.x2())/2,l.theta())
                if ((l.x1()+l.x2())/2)< 160:
                    left_move()
                    img.draw_string(0,0, "Left", color=(0, 255, 0), scale=2)
                else:
                    right_move()
                    img.draw_string(0,0, "Right", color=(0, 255, 0), scale=2)
                time.sleep_ms(30)
                stop()
                time.sleep_ms(30)

            else:
                 print(l.theta())
        lcd.display(img)
except Exception as e:
    sys.print_exception(e)
    lcd.clear(lcd.WHITE)