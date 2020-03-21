import time
from datetime import datetime
try:
    import RPi.GPIO as GPIO
except ImportError:
    from RPiSim.GPIO import GPIO
import os

from lock_door import pin
from lock_door import open_door, is_open, close_door, main

def test_is_open():
    GPIO.cleanup()
    pin = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    hour_open = 7
    hour_close = 22

    GPIO.output(pin, GPIO.LOW)
    assert is_open() == True
    GPIO.output(pin, GPIO.HIGH)
    assert is_open() == False

def test_open_door():
    GPIO.cleanup()
    pin = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    hour_open = 7
    hour_close = 22

    GPIO.output(pin, GPIO.HIGH)
    open_door()
    assert GPIO.input(pin) == 0

    GPIO.output(pin, GPIO.LOW)
    open_door()
    assert GPIO.input(pin) == 0

def test_close_door():
    GPIO.cleanup()
    pin = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    hour_open = 7
    hour_close = 22

    GPIO.output(pin, GPIO.HIGH)
    close_door()
    assert GPIO.input(pin) == 1

    GPIO.output(pin, GPIO.LOW)
    close_door()
    assert GPIO.input(pin) == 1

def test_main():
    # TODO
    pass