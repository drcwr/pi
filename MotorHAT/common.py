from Adafruit_PWM_Servo_Driver import PWM
import time
import ultrasonic_Servo as us

servoMin2 = 114  # Min pulse length out of 4096 180-512 90-307 0-104
servoMax2 = 505  # Max pulse length out of 4096

turnservoMin = 240
turnservoMax = 444
turnservoFront = 353

rightLong = 216 # 30*7.2 50*3.5
leftLong = 231 # 30*7.7  50*3.8


angleMin = 2
angleMax = 178
STEP = 5

pwm = PWM(0x40,debug = False)

def write_pulse2(channel,pulse):
  pulse=max(pulse,servoMin2)
  pulse=min(pulse,servoMax2)
  print "write_pulse2 setPWM pluse: %d " % (pulse)
  pwm.setPWM(channel, 0, pulse)
  #time.sleep(10)
  
G_angle = angleMin - STEP
G_step = STEP
def get_detection_angle():
    global G_angle
    global G_step
    
    G_angle +=  G_step
    if G_angle + G_step > angleMax:
        G_step = -1*STEP
        time.sleep(2)
    if G_angle + G_step < angleMin:
        G_step = STEP
        time.sleep(2)
    G_angle=max(G_angle,angleMin)
    G_angle=min(G_angle,angleMax)
    return G_angle


G_pulse = servoMin2 - STEP + 20
G_step = -1*STEP
def get_detection_pulse():
    global G_pulse
    global G_step
    
    G_pulse +=  G_step
    if G_pulse + G_step > servoMax2:
        G_step = -1*STEP
        # time.sleep(2)
    if G_pulse + G_step < servoMin2:
        G_step = STEP
        # time.sleep(2)
    G_pulse=max(G_pulse,servoMin2)
    G_pulse=min(G_pulse,servoMax2)
    return G_pulse

def loop_detection_pulse():
    pulse = (servoMin2 + servoMax2) /2
    STEP = 1
    step = STEP
    while True:
        pulse=max(pulse,servoMin2)
        pulse=min(pulse,servoMax2)
        distance(pulse)
        #write_pulse2(3, pulse)
        pulse +=  step
        if pulse + step > servoMax2:
            step = -1*STEP
        if pulse + step < servoMin2:
            step = STEP
            
            
def loop_detection_lr():
    pulse = servoMin2
    left = 1
    while True:
        if left == 1 :
            left = 0
            pulse = servoMin2
        else :
            left = 1
            pulse = servoMax2

        pulse=max(pulse,servoMin2)
        pulse=min(pulse,servoMax2)

        write_pulse2(3, pulse)
        time.sleep(10)



