import RPi.GPIO as GPIO
import time

 # GPIO
IN1 = 18      # PUL-
IN2 = 16      # PUL+
IN3 = 15      # DIR-
IN4 = 13      # DIR+
 
def setStep(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)
 
def stop():
    setStep(0, 0, 0, 0)
 
def forward0(delay, steps):  
    for i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)
 
def backward0(delay, steps):  
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
 
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(IN1, GPIO.OUT)      # Set pin's mode is output
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
 

def loop():
    while True:
        print ("backward...")
        backward0(0.0001, 1000)   # 0.0001s   1000
        
        print ("stop...")
        stop()                 # stop
        time.sleep(3)          # sleep 3s
        
        print ("forward...")
        forward0(0.0001, 1000)
        
        print ("stop...")
        stop()
        time.sleep(3)

def destroy():
    GPIO.cleanup()             # 

def backward():
    while True:
        print ("backward...")
        backward0(0.01, 10)   # 0.0001s   1000
        backward0(0.001, 50)   # 0.0001s   1000
        backward0(0.0001, 100)   # 0.0001s   1000
        backward0(0.00002, 10000)   # 0.0001s   1000
        
        print ("stop...")
        stop()                 # stop
        destroy()

def forward():
    while True:
        print ("forward...")
        forward0(0.01, 10)   # 0.0001s   1000
        forward0(0.001, 50)   # 0.0001s   1000
        forward0(0.0001, 100)   # 0.0001s   1000
        forward0(0.00002, 10000)   # 0.0001s   1000
        
        print ("stop...")
        stop()
        destroy()

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        # loop()
        forward()
        # backward()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child function destroy() will be  executed.
        destroy()

