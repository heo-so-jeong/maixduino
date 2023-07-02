from machine import Timer,PWM
import utime
def servo_angle(angle): #angle: -90 ~ 90
    duty = ((angle+90)/180*10+2.5)
    return duty
tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch = PWM(tim, freq=50, duty=0, pin=21)

while True:
    ch.duty(servo_angle(90))
    print(servo_angle(90))
    utime.sleep_ms(5)

