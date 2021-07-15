import subprocess
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
#GPIO.setup(26, GPIO.IN)    # set GPIO25 as input (button)
GPIO.setup(26, GPIO.IN, GPIO.PUD_DOWN)

# wait for the pin to be sorted with GND and, if so, halt the system
#GPIO.wait_for_edge(26, GPIO.FALLING)
while True:
        if GPIO.input(26):
                subprocess.call(['shutdown -h -P now "System halted by GPIO action"'], shell=True)
                exit()
# clean up GPIO on normal exit
GPIO.cleanup()
