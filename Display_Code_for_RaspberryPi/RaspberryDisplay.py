# Author: Yiheng Chang
# Date:   11/24/2020

import time
import board
import neopixel

# GPIO pin 18(PWM) is used to control the LED
pixel_pin = board.D18
# Pixel number is 16
num_pixels = 16

# Initialise a neopixel object
# pixel_pin is 18 num_pixels is 16
# brightness is 0.2(20%) approximately equal to 50
# auto_write set as False hence need pixels.show() every time we send data
# bpp is set as 4 because the RGBW LED is used (or use: pixel_order=(1, 0, 2, 3))
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, bpp = 4)

def pulse_white(color, wait):
    """First, turn on all the LED with even index in order (in color white).
       Then, turn on all the LED with odd index in order (in color white)."""
    # turn on all the LED with even index in order
    for i in range(0, num_pixels, 2):
        pixels[i] = color;
        pixels.show()
        time.sleep(0.1)
    time.sleep(1)

    # turn on all the LED with odd index in order
    for i in range(1, num_pixels, 2):
        pixels[i] = color;
        pixels.show()
        time.sleep(0.1)
    time.sleep(1)

def color_wipe(color, wait):
    """Wipe color across display a pixel at a time."""
    for i in range(num_pixels):
        pixels[i] = color
        pixels.show()
        time.sleep(0.1)
    time.sleep(0.5)


def individual_blink(color, wait):
    """Only one LED blink at one time."""
    for i in range(num_pixels):
        # set all the pixels to black each time an individual LED blink
        for j in range(num_pixels):
            pixels[j] = BLACK
            pixels.show()
        # turn on the individual LED
        pixels[i] = color
        pixels.show()
        time.sleep(wait)
    time.sleep(0.5)

# declare all the color needed as global variables
WHITE = (0, 0, 0, 255)
RED = (255, 0, 0, 0)
GREEN = (0, 255, 0, 0)
BLUE = (0, 0, 255, 0)
BLACK = (0, 0, 0, 0)

while True:
    # First turn off all LEDs
    pixels.fill(BLACK)
    pixels.show()
    time.sleep(1)

    # Execute pulse_white function and wait for 1 second
    pulse_white(WHITE, 0.1)
    time.sleep(1)
    
    # Turn off all LEDs
    pixels.fill(BLACK)
    pixels.show()

    # Execute color_wipe function in RED GREEN BLUE and wait for 1 second
    color_wipe(RED, 0.1)
    color_wipe(GREEN, 0.1)
    color_wipe(BLUE, 0.1)
    time.sleep(1)
    
    # Turn off all LEDs
    pixels.fill(BLACK)
    pixels.show()

    # Execute individual_blink function in white
    individual_blink(WHITE, 0.1)
