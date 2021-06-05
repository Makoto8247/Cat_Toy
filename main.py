import RPi.GPIO as GPIO
from time import sleep

sv = 18 # servo_pin
servo = None

def set():
    global servo
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sv,GPIO.OUT)
    servo = GPIO.PWM(sv,50)
    servo.start(0)

def servo_angle(angle):
    global servo
    duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180
    servo.ChangeDutyCycle(duty)


def loop():
    while True:
        servo_angle(-90)
        sleep(0.1)
        servo_angle(90)
        sleep(0.1)

def main():
    set()
    try:
        while True:
            loop()

    except KeyboardInterrupt:
        pass
    
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
