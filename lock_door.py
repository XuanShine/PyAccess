"""Vérouille la porte d’entrée à partir de 22h, et la dévérouille à partir de 7h
Sachant que: 
- la porte est vérouillée quand les deux fils se touchent
- lorsque il n’y a pas de courant dans le relai, (lorsqu’il est tourné vers le bas: trou en bas, pointe en haut): les trous 2 et 3 se touchent.
- On veut que lorsqu’il n’y a pas de courant, la porte soit dévérouillée.
- le GPIO (BCM) utilisé est le 18
Donc: il faut brancher la porte sur le trou 1 et 2 du relai
Entre 7h et 22h: le GPIO 18 doit être low (donc trou 1 et 2 ne se touchent pas et donc la porte n’est pas vérouillée)
Entre 22h et 7h: le GPIO 18 est high: le trou 1 et 2 se touchent, la porte s’ouvre.
"""

import time
from datetime import datetime
import RPi.GPIO as GPIO
pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

hour_open = 7
hour_close = 22

def open_door():
    GPIO.output(pin, GPIO.LOW)

def is_open():
    return GPIO.input(pin) == 0

def close_door():
    GPIO.output(pin, GPIO.HIGH)


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