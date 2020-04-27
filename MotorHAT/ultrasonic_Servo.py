#!/usr/bin/env python
from Adafruit_PWM_Servo_Driver import PWM
import RPi.GPIO as GPIO
import time
import sys
import common

PWMA   = 18
AIN1   = 22
AIN2   = 27

PWMB   = 23
BIN1   = 25
BIN2   = 24

BtnPin  = 19
Gpin    = 5
Rpin    = 6

TRIG = 20
ECHO = 21
# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40,debug = False)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096


SensorRight = 16
SensorLeft  = 12

def setServoPulse(channel, pulse):
  pulseLength = 1000000.0                   # 1,000,000 us per second
  pulseLength /= 50.0                       # 60 Hz
  #print "%d us per period" % pulseLength
  pulseLength /= 4096.0                     # 12 bits of resolution
  #print "%d us per bit" % pulseLength
  pulse *= 1000.0
  pulse /= (pulseLength*1.0)
# pwmV=int(pluse)
  #print "pluse: %f  " % (pulse)
  pwm.setPWM(channel, 0, int(pulse))

#Angle to PWM
def write(servonum,x):
  y=x/90.0+0.5
  y=max(y,0.5)
  y=min(y,2.5)
  setServoPulse(servonum,y)
  
def t_up(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_up_right(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed/2)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_up_left(speed,t_time):
        L_Motor.ChangeDutyCycle(speed/2)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_stop(t_time):
        L_Motor.ChangeDutyCycle(0)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(0)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def t_down(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

def t_left(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_right(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def keysacn():
    val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == True:
        time.sleep(0.01)
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin,1)
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin,0)
        else:
            GPIO.output(Rpin,0)
            
def setup():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        
        GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
        GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
        GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

        GPIO.setup(AIN2,GPIO.OUT)
        GPIO.setup(AIN1,GPIO.OUT)
        GPIO.setup(PWMA,GPIO.OUT)
        
        GPIO.setup(BIN1,GPIO.OUT)
        GPIO.setup(BIN2,GPIO.OUT)
        GPIO.setup(PWMB,GPIO.OUT)
        pwm.setPWMFreq(50)                        # Set frequency to 60 Hz
 
        GPIO.setup(SensorRight,GPIO.IN)
        GPIO.setup(SensorLeft,GPIO.IN)


def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    
    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100

sleepTime = 0.06

def front_detection():
        write(0,90)
        time.sleep(sleepTime)
        dis_f = distance()
        return dis_f

def left_detection():
         write(0, 175)
         time.sleep(sleepTime)
         dis_l = distance()
         return dis_l
        
def right_detection():
        write(0,5)
        time.sleep(sleepTime)
        dis_r = distance()
        return dis_r

def num_detection(num):
        write(0,num)
        time.sleep(sleepTime)
        dis = distance()
        return int(dis)

def loop_detection():
        num = 5
        while True:
            dis = num_detection(num)
            print "num %d dis: %d  " % (num,dis)
            num += 5
            num %= 170

dst_arr = [5,30,60,90,120,150,175]

def isup(dst_arr):
    if (dst_arr[2] > 50) == True and (dst_arr[3] > 50) == True and (dst_arr[4] > 50) == True:
        return True

def isleft(dst_arr):
    if (dst_arr[6] > 30) == True and (dst_arr[5] > 30) == True and (dst_arr[1] < dst_arr[5]*2) == True:
        return True

def isright(dst_arr):
    if (dst_arr[0] > 30) == True and (dst_arr[1] > 30) == True :
        return True

rtol = 1
def get_detection():
    print "get_detection_front" 
    global rtol
    if rtol == 1:
        rtol = 0
        dst_arr[0] = 0 #num_detection(5) # right
        dst_arr[1] = 0 #num_detection(30)
        dst_arr[2] = num_detection(70)
        dst_arr[3] = num_detection(90)
        dst_arr[4] = num_detection(110)
        dst_arr[5] = 0 #num_detection(150)
        dst_arr[6] = 0 #num_detection(175)
    else:
        rtol = 1
        dst_arr[6] = 0 #num_detection(175) # left
        dst_arr[5] = 0 #num_detection(150)
        dst_arr[4] = num_detection(110)
        dst_arr[3] = num_detection(90)
        dst_arr[2] = num_detection(70)
        dst_arr[1] = 0 #num_detection(30)
        dst_arr[0] = 0 #num_detection(5)
    print dst_arr

def get_detection_all():
    print "get_detection_all"
    global rtol
    global sleepTime
    sleepTime = 0.07
    if rtol == 1:
        rtol = 0
        dst_arr[0] = num_detection(10) # right
        dst_arr[1] = num_detection(20)
        dst_arr[2] = 0 #num_detection(50)
        dst_arr[3] = 0 #num_detection(90)
        dst_arr[4] = 0 #num_detection(130)
        dst_arr[5] = num_detection(160)
        dst_arr[6] = num_detection(170)
    else:
        rtol = 1
        dst_arr[6] = num_detection(170) # left
        dst_arr[5] = num_detection(160)
        dst_arr[4] = 0 #num_detection(130)
        dst_arr[3] = 0 #num_detection(90)
        dst_arr[2] = 0 #num_detection(50)
        dst_arr[1] = num_detection(20)
        dst_arr[0] = num_detection(10)
    print dst_arr
    
def get_detection_left():
    print "get_detection_left"
    global rtol
    if rtol == 1:
        rtol = 0
        dst_arr[0] = 0
        dst_arr[1] = 0
        dst_arr[2] = 0
        dst_arr[3] = 0
        dst_arr[4] = 0
        dst_arr[5] = num_detection(160)
        dst_arr[6] = num_detection(170)
    else:
        rtol = 1
        dst_arr[0] = 0
        dst_arr[1] = 0
        dst_arr[2] = 0
        dst_arr[3] = 0
        dst_arr[4] = 0
        dst_arr[6] = num_detection(170) # left
        dst_arr[5] = num_detection(160)
    print dst_arr
        
def get_detection_right():
    print "get_detection_right"
    global rtol
    if rtol == 1:
        rtol = 0
        dst_arr[0] = num_detection(10) # right
        dst_arr[1] = num_detection(20)
        dst_arr[5] = 0
        dst_arr[6] = 0
        dst_arr[2] = 0
        dst_arr[3] = 0
        dst_arr[4] = 0
    else:
        rtol = 1
        dst_arr[1] = num_detection(20)
        dst_arr[0] = num_detection(10)
        dst_arr[5] = 0
        dst_arr[6] = 0
        dst_arr[2] = 0
        dst_arr[3] = 0
        dst_arr[4] = 0
    print dst_arr
        
def stop():
    t_stop(0.1)
    
left = 1

def changedetectionspeed():
    global sleepTime
    if dst_arr[3] > 90 == True :
        sleepTime = 0.12
    else :
        sleepTime = 0.07


def loop():
    global left

    while True:
        get_detection()
        if isup(dst_arr) == True:
            changedetectionspeed()
            t_up(40,0)
            left = 1
        else :
            stop()
            turn()


def looprl():
    global left
    while True:
        get_detection()
        if isup(dst_arr) == True:
            turn_front()
            changedetectionspeed()
            t_up(30,0)
            left = 1
        else :
            #stop()
            if left == 0 :
                get_detection_right()
            elif left == 2 :
                get_detection_left()
            else :
                get_detection_all()
            #get_detection_all()
            if isleft(dst_arr) == True :
                t_up(30,0)
                turn_left()
                left = 2
            elif isright(dst_arr) == True :
                t_up(30,0)
                turn_right()
                left = 0
            else :
                turn_front()
                t_down(30,0)
                left = 1
                #t_stop(0.2)
                get_detection_all()
                #t_up(30,0)
                if isleft(dst_arr) == True :
                    t_up(30,0)
                    turn_left()
                elif isright(dst_arr) == True :
                    t_up(30,0)
                    turn_right()


def looprl_turn():
    global left
    while True:
        get_detection()
        if isup(dst_arr) == True:
            turn_front()
            changedetectionspeed()
            t_up(30,0)
            left = 1
        else :
            #stop()
            if left == 0 :
                get_detection_right()
            elif left == 2 :
                get_detection_left()
            else :
                get_detection_all()
            #get_detection_all()
            if isleft(dst_arr) == True :
                turn_left()
                t_up_left(40,0)
                left = 2
            elif isright(dst_arr) == True :
                turn_right()
                t_up_right(40,0)
                left = 0
            else :
                turn_front()
                t_down(30,0)
                left = 1
                #t_stop(0.2)
                get_detection_all()
                #t_up(30,0)
                if isleft(dst_arr) == True :
                    turn_left()
                    t_up_left(40,0)
                elif isright(dst_arr) == True :
                    turn_right()
                    t_up_right(40,0)


def write_pulse(channel,pulse):
  pulse=max(pulse,servoMin)
  pulse=min(pulse,servoMax)
  #print "setPWM pluse: %d " % (pulse)
  pwm.setPWM(channel, 0, pulse)
 
def distance_pulse(pulse):
        write_pulse(0, pulse)
        #write_pulse(1, pulse)
        #write(2, num%30)
        time.sleep(0.01)
        dis = distance()
        print "------- pulse %d dis: %d  " % (pulse,dis)
        if dis < 50:
            time.sleep(0.03)


def destroy():
    print "cleanup"
    GPIO.cleanup()

def initbrd():
        setup()
        L_Motor= GPIO.PWM(PWMA,100)
        L_Motor.start(0)
        R_Motor = GPIO.PWM(PWMB,100)
        R_Motor.start(0)
        # keysacn()
        
def loop_detection_lr():
    pulse = common.servoMin2
    left = 1
    while True:
        #distance(pulse)
        if left == 1 :
            left = 0
            pulse = common.servoMin2
            t_up(20,0)
        else :
            left = 1
            pulse = common.servoMax2
            t_down(20,0)

        pulse=max(pulse,common.servoMin2)
        pulse=min(pulse,common.servoMax2)

        common.write_pulse2(3, pulse)
        time.sleep(15)

def turn_left():
    common.write_pulse2(3, common.turnservoMin)

def turn_right():
    common.write_pulse2(3, common.turnservoMax)

def turn_front():
    common.write_pulse2(3, common.turnservoFront)

def loopudrl():
    while True:
        turn_front()
        t_up(30,3)
        t_stop(1)
        t_down(30,3)
        t_stop(1)

        turn_right()
        t_up_right(50,3.5)
        t_stop(1)

        turn_left()
        t_up_left(50,3.7)
        t_stop(1)


if __name__ == "__main__":
        setup()
        L_Motor= GPIO.PWM(PWMA,100)
        L_Motor.start(0)
        R_Motor = GPIO.PWM(PWMB,100)
        R_Motor.start(0)
        keysacn()
        try:
                #loop_detection()
                #loop()
                #loop_detection_lr()
                # looprl()
                # loopudrl()
                looprl_turn()
        except KeyboardInterrupt:
                front_detection()
                t_stop(1)
                destroy()




