import RPi.GPIO as GPIO
import os
import subprocess
from time import sleep

sv = 18 # servo_pin
SPI_cs = 8 # cs/shdn
SPI_miso = 9 # Dout
SPI_mosi = 10 # Din
SPI_clk = 11 # clk
button = 23
servo = None

def set():
    global servo
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sv,GPIO.OUT)
    GPIO.setup(SPI_clk,GPIO.OUT)
    GPIO.setup(SPI_mosi,GPIO.OUT)
    GPIO.setup(SPI_miso,GPIO.IN)
    GPIO.setup(SPI_cs,GPIO.OUT)
    GPIO.setup(button,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    servo = GPIO.PWM(sv,50)
    servo.start(0)

def readadc(adccha,clockpin,mosipin,misopin,cspin):
    if adccha > 7 or adccha < 0:
        return -1
    GPIO.output(cspin,GPIO.HIGH)
    GPIO.output(clockpin,GPIO.LOW)
    GPIO.output(cspin,GPIO.LOW)

    commandout = adccha
    commandout |= 0x18
    commandout <<= 3

    for i in range(5):
        if commandout & 0x80:
            GPIO.output(mosipin,GPIO.HIGH)
        else:
            GPIO.output(mosipin,GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin,GPIO.HIGH)
        GPIO.output(clockpin,GPIO.LOW)
    adcout = 0
    for i in range(13):
        GPIO.output(clockpin,GPIO.HIGH)
        GPIO.output(clockpin,GPIO.LOW)
        adcout <<= 1
        if i > 0 and GPIO.input(misopin) == GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin,GPIO.HIGH)
    return adcout

def servo_angle(angle):
    global servo
    duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180
    servo.ChangeDutyCycle(duty)


def loop():
    inputVal = readadc(0,SPI_clk,SPI_mosi,SPI_miso,SPI_cs)
    sleep_time = round(inputVal / 4095,3)
    servo_angle(-90)
    sleep(sleep_time)
    servo_angle(90)
    sleep(sleep_time)
    if GPIO.input(button) == 1:
        raise KeyboardInterrupt("shutdown")

def main():
    set()
    try:
        while True:
            loop()

    except KeyboardInterrupt as e:
        print(e)
    
    finally:
        GPIO.cleanup()
        subprocess.run(["sudo","shutdown","-h","now"])

if __name__ == "__main__":
    main()
