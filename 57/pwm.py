# https://blog.csdn.net/weixin_42337765/article/details/122424152

import RPi.GPIO as GPIO
import time
 
TERMINAL1 = 38 # PUL +
TERMINAL2 = 35 # DIR +
 
def setup():
    # init
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TERMINAL1, 0)
    GPIO.setup(TERMINAL2, 0)
 
def start(pulse_terminal):
    # start
    pulse_terminal.start(0)
    pulse_terminal.ChangeDutyCycle(50) # hz 0~100
 
def stop(pulse_terminal):
    # stop
    pulse_terminal.stop()
 
def set_direction(direction=1):
    GPIO.output(TERMINAL2, direction) # high low
 
if __name__ == '__main__':     # Program start from here
    setup()
 
    pulse_terminal = GPIO.PWM(TERMINAL1, 1000) # pul
 
    set_direction(1)
    start(pulse_terminal)
    time.sleep(3)
    stop(pulse_terminal)
    time.sleep(3)
    set_direction(0)
    start(pulse_terminal)
    time.sleep(3)
 
    GPIO.cleanup()