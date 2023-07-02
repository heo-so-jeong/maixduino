import KPU as kpu
import sensor
import lcd
from Maix import GPIO
from fpioa_manager import fm
from board import board_info
from machine import Timer,PWM
import time
import gc

############### config #################
class_num = 2
sample_num = 20
THRESHOLD = 11
class_names = ['Mask', 'No Mask', 'class3']
board_cube = 0
########################################


def draw_string(img, x, y, text, color, scale, bg=None ):
    if bg:
        img.draw_rectangle(x-2,y-2, len(text)*8*scale+4 , 16*scale, fill=True, color=bg)
    img = img.draw_string(x, y, text, color=color,scale=scale)
    return img

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
if board_cube == 1:
    sensor.set_vflip(True)
    sensor.set_hmirror(True)
    lcd.init(type=2)
    lcd.rotation(2)
else:
    lcd.init()

fm.register(21, fm.fpioa.GPIOHS0)
key = GPIO(GPIO.GPIOHS0, GPIO.IN ,GPIO.PULL_UP)

tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch = PWM(tim, freq=261, duty=0, pin=22)

um =  [261,293,329,349,391,440,493]

try:
    del model
except Exception:
    pass
try:
    del classifier
except Exception:
    pass
gc.collect()
model = kpu.load(0x300000)
classifier = kpu.classifier(model, class_num, sample_num)

cap_num = 0
train_status = 0
last_cap_time = 0
last_btn_status = 1
while 1:
    img = sensor.snapshot()
    if board_cube:
        img = img.rotation_corr(z_rotation=90)
        img.pix_to_ai()
    # capture img
    if train_status == 0:
        if key.value() == 0:
            time.sleep_ms(30)
            if key.value() == 0 and (last_btn_status == 1) and (time.ticks_ms() - last_cap_time > 500):
                last_btn_status = 0
                last_cap_time = time.ticks_ms()
                if cap_num < class_num:
                    index = classifier.add_class_img(img)
                    cap_num += 1
                    print("add class img:", index)
                elif cap_num < class_num + sample_num:
                    index = classifier.add_sample_img(img)
                    cap_num += 1
                    print("add sample img:", index)
            else:
                img = draw_string(img, 2, 200, "release boot key please", color=lcd.WHITE,scale=1, bg=lcd.RED)
        else:
            time.sleep_ms(30)
            if key.value() == 1 and (last_btn_status == 0):
                last_btn_status = 1
            if cap_num < class_num:
                img = draw_string(img, 0, 200, "press key to capture "+class_names[cap_num], color=lcd.WHITE,scale=1, bg=lcd.RED)
            elif cap_num < class_num + sample_num:
                img = draw_string(img, 0, 200, "press key to capture sample{}".format(cap_num-class_num), color=lcd.WHITE,scale=1, bg=lcd.RED)
    # train and predict
    if train_status == 0:
        if cap_num >= class_num + sample_num:
            print("start train")
            img = draw_string(img, 30, 100, "training...", color=lcd.WHITE,scale=2, bg=lcd.RED)
            lcd.display(img)
            classifier.train()
            print("train end")
            train_status = 1
    else:
        res_index = -1
        try:
            res_index, min_dist = classifier.predict(img)
            print("{:.2f}".format(min_dist))
        except Exception as e:
            print("predict err:", e)
        if res_index >= 0 and min_dist < THRESHOLD :
            print("predict result:", class_names[res_index])
            img = draw_string(img, 2, 2, class_names[res_index], color=lcd.WHITE,scale=2, bg=lcd.RED)
        else:
            print("unknown, maybe:", class_names[res_index])
            img = draw_string(img, 2, 2, 'maybe {}'.format(class_names[res_index]), color=lcd.WHITE,scale=2, bg=lcd.RED)
            if res_index == 1: ## No Mask
                ch.duty(50)
                ch.freq(um[4])
            else:
                ch.duty(0)
    lcd.display(img)

# You can save trained data to file system by:
classifier.save("3_classes.classifier")

# Then load :
# model = kpu.load(0x300000)
# classifier = kpu.classifier.load(model, "3_class.classifier")
