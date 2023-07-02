import time, network
from Maix import GPIO
from fpioa_manager import fm

class wifi():
    # IO map for ESP32 on Maixduino
    fm.register(25,fm.fpioa.GPIOHS10)#cs
    fm.register(8,fm.fpioa.GPIOHS11)#rst
    fm.register(9,fm.fpioa.GPIOHS12)#rdy
    print("Use Hareware SPI for other maixduino")
    fm.register(28,fm.fpioa.SPI1_D0, force=True)#mosi
    fm.register(26,fm.fpioa.SPI1_D1, force=True)#miso
    fm.register(27,fm.fpioa.SPI1_SCLK, force=True)#sclk
    nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10, rst=fm.fpioa.GPIOHS11, rdy=fm.fpioa.GPIOHS12, spi=1)

print("ESP32_SPI firmware version:", wifi.nic.version())

while True:
    try:
        # get ADC0~5
        adc = wifi.nic.adc((0,1))
    except Exception as e:
        print(e)
        continue
    print("ADC0 Value : %04d" %adc[1])

