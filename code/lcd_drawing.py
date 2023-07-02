import lcd
import image
import utime

lcd.init()
img=image.Image()
img.draw_circle((100,100,100),color=(0,255,0),fill=True)
lcd.display(img)
utime.sleep(1)
img.draw_rectangle((100,100,200,70),color=(255,0,0),fill=True)
lcd.display(img)
utime.sleep(1)
img.draw_line((0,0,lcd.width(),lcd.height()),thickness=3,color=(0,0,255))
lcd.display(img)
utime.sleep(1)
img.draw_string(100,100,'hello changho',scale=2)
lcd.display(img)
utime.sleep(1)
lcd.clear()

