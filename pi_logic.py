import subprocess
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN, GPIO.PUD_DOWN)

while True:
        if GPIO.input(26):
                
                #INSERT WHATEVER CODE YOU WANT TO RUN BEFORE SHUTDOWN HERE, THE NEXT LINE SHUTS OFF THE PI
                subprocess.call(['shutdown -h -P now "System halted by GPIO action"'], shell=True)
                exit()

GPIO.cleanup()
