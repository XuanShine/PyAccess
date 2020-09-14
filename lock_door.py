"""Vérouille la porte d’entrée à partir de 22h, et la dévérouille à partir de 7h
Sachant que: 
- la porte est vérouillée quand les deux fils se touchent
- lorsque il n’y a pas de courant dans le relai, (lorsqu’il est tourné vers le bas: trou en bas, pointe en haut): les trous 2 et 3 se touchent.
- On veut que lorsqu’il n’y a pas de courant, la porte soit dévérouillée.
- le GPIO (BCM) utilisé est le 5
Donc: il faut brancher la porte sur le trou 1 et 2 du relai

Entre 7h et 22h: le GPIO 5 doit être HIGH (donc trou 1 et 2 ne se touchent pas et donc la porte n’est pas vérouillée)
Entre 22h et 7h: le GPIO 5 est LOW: le trou 1 et 2 se touchent, la porte se vérouille.

INFORMATIONS:
Lorsque le waveshare est initialisé, il est automatiquement en LOW. En LOW, le petit témoin du waveshare est allumé, et le pin A et C (1 et 2) se touchent.
Lorsque le waveshare n'est pas fourni en courant, ou bien que les GPIO ont été "cleanup", le petit témoin est éteint et le pin C et B (2 et 3) se touchent.

Comme les fils électriques ont été branchés sur le pin A et C (1 et 2), ils se toucheront quand le GPIO sera en position LOW.

"""

import time
from datetime import datetime
try:
    import RPi.GPIO as GPIO
except ImportError:
    from RPiSim.GPIO import GPIO
import logging
import os
"   "
C = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(filename=os.path.join(C, "lock_door.log"), level=logging.DEBUG, format="%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

relai = { 1: 5,  # porte entrée
            2: 6,  # lumières enseignes
            3: 13,  # lumières out-receptions
            4: 16,  # lumières porches (ext)
            5: 19,  # lumières in-reception
            6: 20,  # lumières banque
            7: 21,  # lumières salle petit-déj buffet
            8: 26 } # lumières salle petit-déj tables
hour_open = 7
hour_close = 22
schedule_hour = {
    2: (6, 19, "off"),
    3: (7, 23, "on"),
    4: (8, 18, "off"),
    5: (12, 15, "off"),
    6: (15, 22, "on"),
    7: (7, 23, "on"),
    8: (7, 11, "on")    
}

def init_GPIO():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    [GPIO.setup(relai_i, GPIO.OUT) for relai_i in relai.values()]
    # ouverture de porte (pin 1) de facto:
    GPIO.output(relai[1], GPIO.HIGH)
    # les autres relai devraient être en LOW donc les pin 1 et 2 (A et C)
    # se touchent donc les lampes sont allumées.


def open_door():
    GPIO.output(relai[1], GPIO.HIGH)
    logging.info("Door Opened")

def is_open():
    return GPIO.input(relai[1]) == GPIO.HIGH

def close_door():
    GPIO.output(relai[1], GPIO.LOW)
    logging.info("Door Closed")

def turn(state, relai_ch):
    if state == "on":
        GPIO.output(relai[relai_ch], GPIO.LOW)
    else:
        GPIO.output(relai[relai_ch], GPIO.HIGH)
    logging.info(f"{relai_ch} : {state}")

def is_on(relai_ch):
    return GPIO.input(relai[relai_ch]) != 0

def init_lamp():
    for relai_ch in schedule_hour.keys():
        h_top = schedule_hour[relai_ch][0]
        h_bot = schedule_hour[relai_ch][1]
        state = schedule_hour[relai_ch][2]
        anti_state = "off" if state == "on" else "on"
        if h_top <= datetime.now().hour < h_bot:
            turn(state, relai_ch)
        else:
            turn(anti_state, relai_ch)


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
    pass