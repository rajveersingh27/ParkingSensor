# Import required Python libraries
import RPi.GPIO as GPIO
import time

# We will be using the BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Select which GPIOs you will use
GPIO_BUZZER = 3
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_LED = 2

# Set BUZZER to OUTPUT mode
GPIO.setup(GPIO_BUZZER, GPIO.OUT)
# Set TRIGGER to OUTPUT mode
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
# Set ECHO to INPUT mode
GPIO.setup(GPIO_ECHO, GPIO.IN)
# Set LED to OUTUT mode
GPIO.setup(GPIO_LED, GPIO.OUT)

# Measures the distance between a sensor and an obstacle and returns the measured value
def distance():
  # Send 10 microsecond pulse to TRIGGER
  GPIO.output(GPIO_TRIGGER, True) # set TRIGGER to HIGH
  time.sleep(0.00001) # wait 10 microseconds
  GPIO.output(GPIO_TRIGGER, False) # set TRIGGER back to LOW
 
  # Create variable start and assign it current time
  start = time.time()
  # Create variable stop and assign it current time
  stop = time.time()
  # Refresh start value until the ECHO goes HIGH = until the wave is send
  while GPIO.input(GPIO_ECHO) == 0:
    start = time.time()
 
  # Assign the actual time to stop variable until the ECHO goes back from HIGH to LOW = the wave came back
  while GPIO.input(GPIO_ECHO) == 1:
    stop = time.time()
 
  # Calculate the time it took the wave to travel there and back
  measuredTime = stop - start
  # Calculate the travel distance by multiplying the measured time by speed of sound
  distanceBothWays = measuredTime * 33112 # cm/s in 20 degrees Celsius
  # Divide the distance by 2 to get the actual distance from sensor to obstacle
  distance = distanceBothWays / 2

  # Print the distance to see if everything works correctly
  print("Distance : {0:5.1f}cm".format(distance))
  # Return the actual measured distance
  return distance

# Calculates the frequency of beeping depending on the measured distance
def beep_freq():
  # Measure the distance
  dist = distance()
  # If the distance is bigger than 50cm, we will not beep at all
  if dist > 50:
    return -1
  # If the distance is between 50 and 30 cm, we will beep once a second
  elif dist <= 50 and dist >=30:
    return 1
  # If the distance is between 30 and 20 cm, we will beep every twice a second
  elif dist < 30 and dist >= 20:
    
    return 0.5
  # If the distance is between 20 and 10 cm, we will beep four times a second
  elif dist < 20 and dist >= 10:
    return 0.25
  # If the distance is smaller than 10 cm, we will beep constantly
  else:
    return 0

# Main function
def main():
  try:
    # Repeat till the program is ended by the user
    while True:
      # Get the beeping frequency
      freq = beep_freq()
      # No beeping
      if freq == -1:
        GPIO.output(GPIO_BUZZER, False)
        time.sleep(0.25)
      # Constant beeping
      elif freq == 0:
        GPIO.output(GPIO_LED, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(GPIO_LED, GPIO.LOW)
        GPIO.output(GPIO_BUZZER, True)
        time.sleep(0.25)
      # Beeping on certain frequency
      else:
        GPIO.output(GPIO_LED, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(GPIO_LED, GPIO.LOW)
        GPIO.output(GPIO_BUZZER, True)
        time.sleep(0.2) # Beep is 0.2 seconds long
        GPIO.output(GPIO_BUZZER, False)
        time.sleep(freq) # Pause between beeps = beeping frequency
  # If the program is ended, stop beeping and cleanup GPIOs
  except KeyboardInterrupt:
    GPIO.output(GPIO_BUZZER, False)
    GPIO.cleanup()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()