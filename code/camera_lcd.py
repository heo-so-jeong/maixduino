import sensor, image, time, lcd

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

lcd.init(freq=15000000)
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    lcd.display(img)
    print(clock.fps())
