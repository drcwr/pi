from Adafruit_PWM_Servo_Driver import PWM
import time
import ultrasonic_Servo as us
import common
import RPi.GPIO as GPIO

# import g
# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40,debug = False)

servoMin = 150  # Min pulse length out of 4096 // 180-512 90-307 0-104
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
  print "pluse: %f  " % (pulse)
  pwm.setPWM(channel, 0, int(pulse))

def write_pulse(channel,pulse):
  # pulse=max(pulse,servoMin)
  # pulse=min(pulse,servoMax)
  #print "setPWM pluse: %d " % (pulse)
  pwm.setPWM(channel, 0, pulse)


  
#Angle to PWM
def write(servonum,x):
  y=x/90.0+0.5
  y=max(y,0.5)
  y=min(y,2.5)
  # print "write angle: %d  " % x
  setServoPulse(servonum,y)

def distance(pulse):
        write_pulse(0, pulse)
        #write_pulse(1, pulse)
        #write(2, num%30)
        time.sleep(0.01)
        dis = us.distance()
        print "------- pulse %d dis: %d  " % (pulse,dis)
        if dis < 50:
            time.sleep(0.03)


def loop_detection():
    while True:
        write(0, 180)
        time.sleep(1)
        dis = us.distance()
        print "dis: %d  " % dis
        write(0, 150)
        time.sleep(1)
        dis = us.distance()
        print "dis: %d  " % dis
        write(0, 120)
        time.sleep(1)
        dis = us.distance()
        print "dis: %d  " % dis
        write(0,90)
        time.sleep(1)
        dis = us.distance()
        print "90 dis: %d  " % dis
        write(0,1)
        time.sleep(1)
        dis = us.distance()
        print "1 dis: %d  " % dis
        # distance(30)


def loop_detection_angle():
    while True:
      angle = common.get_detection_angle()
      write(0, angle)
      time.sleep(0.2)
      dis = us.distance()
      print "angle-dis: %d %d  " % (angle,dis)
      # print ""
      time.sleep(0.05)      

def loop_detection_pulse():
  write_pulse(0, 150)
  time.sleep(0.05)
  while True:
    pulse = common.get_detection_pulse()
    write_pulse(0, pulse)
    time.sleep(0.02)
    dis = us.distance()
    print "pulse--dis: %d %d  " % (pulse,dis)
    # print ""
    if   pulse == common.servoMin2 or pulse == common.servoMax2 :
      time.sleep(5)
    time.sleep(0.01)      


pwm.setPWMFreq(50)                        # Set frequency to 60 Hz
#pwm.setPWM(0,0,153)
us.initbrd()

def sensor():
  while True:
    SR_2 = GPIO.input(SensorRight)
    SL_2 = GPIO.input(SensorLeft)
    if SL_2 == True and SR_2 == True:
        print "t_up"
    elif SL_2 == True and SR_2 ==False:
        print "Left"
    elif SL_2==False and SR_2 ==True:
        print "Right"
    else :
        print "down"
  
try:
        # loop_detection()
        # loop_detection_angle()
        loop_detection_pulse()
        # sensor()
except KeyboardInterrupt:
        us.destroy()
        #us.t_stop(1)
  #while (True):
  # Change speed of continuous servo on channel O
#  setServoPulse(0, 2)
#  time.sleep(3)
#  setServoPulse(0, servoMax)
#  time.sleep(3000)



