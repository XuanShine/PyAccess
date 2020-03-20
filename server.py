from flask import Flask, escape, request

import schedule
import time
from threading import Thread

import lock_door
from lock_door import *


# schedule
tasks = dict()
hour_on_off = [7, 22]

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

app = Flask(__name__)

@app.route('/exemple')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/set_state')
def set_state(state: str, wait_time=3600):
    """state can be 'on' on 'off' """
    if state == "on":
        open_door()
    else:
        close_door()
    schedule.cancel_job(tasks["on"])
    schedule.cancel_job(tasks["off"])
    schedule.cancel_job(tasks["auto"])

    def restart_jobs():
        # TODO: prendre en compte les modifications qui peuvent être faites pendant le temps de pause
        time.sleep(wait_time)
        tasks["on"] = schedule.every().day.at(f"{hour_on_off[0]}:00").do(open_door)
        tasks["off"] = schedule.every().day.at(f"{hour_on_off[1]}:00").do(close_door)
        tasks["auto"] = schedule.every().hour.run(lock_door.main, *hour_on_off) 

    t2 = Thread(target=restart_jobs)
    t2.start()

@app.route("/get_state")
def get_state():
    return "open" if is_open() else "close"

@app.route("/set_state_hour")
def set_state_hour(state, hour):
    """
    <state> : "on" "off" "auto" 
    <hour> : int, but is ignore if state == auto
    """
    if state == "auto":
        schedule.cancel_job(tasks["on"])
        schedule.cancel_job(tasks["off"])
        schedule.cancel_job(tasks["auto"])
        tasks["on"] = schedule.every().day.at(f"7:00").do(open_door)
        tasks["off"] = schedule.every().day.at(f"22:00").do(close_door)
        tasks["auto"] = schedule.every().hour.run(lock_door.main, 7, 22)
    else:
        schedule.cancel_job(tasks["auto"])
        if state == "on":
            schedule.cancel_job(tasks["on"])
            hour_on_off[0] = hour
            tasks["on"] = schedule.every().day.at(f"{hour}:00").do(open_door)
        elif state == "off":
            hour_on_off[1] = hour
            schedule.cancel_job(tasks["off"])
            tasks["off"] = schedule.every().day.at(f"{hour}:00").do(close_door)
        
        tasks["auto"] = schedule.every().hour.run(lock_door.main, *hour_on_off) 

    return f"Heures ouvert, fermé: {hour_on_off}"

@app.route("/get_state_hour")
def get_state_hour():
    """
    RETURN: { "on" : <int>
              "off": <int> }
    """
    return {"on": hour_on_off[0], "off": hour_on_off[1]}

if __name__ == "__main__":
    sched = Thread(target=run_schedule)
    sched.start()
    tasks["on"] = schedule.every().day.at(f"7:00").do(lock_door.open_door)
    tasks["off"] = schedule.every().day.at(f"22:00").do(lock_door.close_door)

    app.start()