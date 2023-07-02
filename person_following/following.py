import sensor, image, lcd, time
from Maix import GPIO
from fpioa_manager import fm
from board import board_info
from machine import Timer,PWM
import gc, sys
import KPU as kpu

lcd.init()
try:
    sensor.reset()
except Exception as e:
    raise Exception("please check hardware connection, or hardware damaged! err: {}".format(e))
sensor.set_hmirror(False)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(time = 2000)
sensor.set_vflip(1)

lcd.init(type=1)
lcd.rotation(0)
lcd.clear(lcd.WHITE)

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

anchors = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)

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

def move():
    ch1.duty(0)
    ch2.duty(90)
    ch3.duty(90)
    ch4.duty(0)

try:
    img = sensor.snapshot()
    lcd.display(img)
except Exception:
    img.clear()
    img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
    lcd.display(img)

state_previous = 1
count = 0

try:
    task = None
    task = kpu.load(0x300000)
    kpu.init_yolo2(task, 0.5, 0.3, 5, anchors)
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

        img = sensor.snapshot()
        t = time.ticks_ms()
        objects = kpu.run_yolo2(task, img)
        t = time.ticks_ms() - t
        if objects:
            for obj in objects:
                img.draw_rectangle(obj.rect())
                rect_x = obj.rect()[0]
                rect_width = obj.rect()[2]
                rect_height = obj.rect()[3]
                if rect_height>112:
                    img.draw_string(0,0, "too close.." , scale=2)
                    stop()
                else:
                    if(rect_x+rect_width)/2<112:# face가 왼쪽에 있으면
                        right_move()
                    else:  #face가 오른쪽에 있으면
                        left_move()
                time.sleep_ms(30)
                move()
                time.sleep_ms(30)
        else:
            stop()
                #print(obj.rect()[2]) #obj dictionary is not class  rect()[0] : x [1] : y
        img.draw_string(0, 200, "t:%dms" %(t), scale=2)
        lcd.display(img)
except Exception as e:
    sys.print_exception(e)
    lcd.clear(lcd.WHITE)