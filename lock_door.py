"""Vérouille la porte d’entrée à partir de 22h, et la dévérouille à partir de 7h
Sachant que: 
- la porte est vérouillée quand les deux fils se touchent
- lorsque il n’y a pas de courant dans le relai, (lorsqu’il est tourné vers le bas: trou en bas, pointe en haut): les trous 2 et 3 se touchent.
- On veut que lorsqu’il n’y a pas de courant, la porte soit dévérouillée.
- le GPIO (BCM) utilisé est le 5
Donc: il faut brancher la porte sur le trou 1 et 2 du relai
Entre 7h et 22h: le GPIO 5 doit être low (donc trou 1 et 2 ne se touchent pas et donc la porte n’est pas vérouillée)
Entre 22h et 7h: le GPIO 5 est high: le trou 1 et 2 se touchent, la porte se vérouille.
"""

import time
from datetime import datetime
try:
    import RPi.GPIO as GPIO
except ImportError:
    from RPiSim.GPIO import GPIO
import logging
import os

C = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(filename=os.path.join(C, "lock_door.log"), level=logging.DEBUG, format="%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

pin_door = 5  # channel 1  serrure porte d’entrée
pin_2 = 6  # ch2  lumières extérieurs
pin_3 = 13  # ch3  lumières réceptions
pin_4 = 16  # ch4  lumières paliers
pin_5 = 19  # ch5  lumières salle petit-dej
pin_6 = 20  # ch6
pin_7 = 21  # ch7
pin_8 = 26  # ch8
pin = pin_door
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

hour_open = 7
hour_close = 22

def open_door():
    GPIO.output(pin, GPIO.LOW)
    logging.info("Door Opened")

def is_open():
    return GPIO.input(pin) == 0

def close_door():
    GPIO.output(pin, GPIO.HIGH)
    logging.info("Door Closed")

def turn(state, pin):
    if state == "on":
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)
    logging.info(f"{pin} : {state}")

def is_on(pin):
    return GPIO.input(pin) != 0


def main(hour_open=hour_open, hour_close=hour_close):
    if hour_open <= datetime.now().hour < hour_close:  # open
        if not is_open():
            open_door()
    else:
        if is_open():
            close_door()
    # GPIO.cleanup()

if __name__ == "__main__":
    main()