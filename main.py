# Camel Case < Snake Case
from win32gui import GetForegroundWindow
import psutil
import time
import win32process
import datetime
import signal
import sys
import json
import threading

# save all data call on exit & on day change

# Global Vars
process_time={} 
timestamp = {}
current_date = datetime.date.today()

stop_event = threading.Event()
rollover_timer = None

def rollover_day():
    global current_date
    if stop_event.is_set():
        return
    # Save old data to file
    print(current_date)

    current_date = datetime.date.today()

    # Create new date and Dict
    print(current_date)

    schedule_rollover()

def schedule_rollover():
    global rollover_timer
    now = datetime.datetime.now()

    tomorrow = (now + datetime.timedelta(days = 1)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    delay = (tomorrow - now).total_seconds()
    print(delay)
    rollover_timer = threading.Timer(delay, rollover_day)
    rollover_timer.daemon = True
    rollover_timer.start()

def record_time():
    """
    Adds The current app to a dictionary and adds the time on each!
    """
    try:
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
        timestamp[current_app] = int(time.time())
        time.sleep(1)
        if current_app not in process_time.keys():
            process_time[current_app] = 0
        process_time[current_app] = process_time[current_app]+int(time.time())-timestamp[current_app]
    except Exception as e :
        print(e)
        time.sleep(1)
        
def on_exit(signum, frame):
    """
    Runs when the program is closed using CTRL C or Terminated
    """
    print("Shutting Down")

    stop_event.set()
    if rollover_timer:
        rollover_timer.cancel()

    if newDate:
        data["sessions"].append({"date": currentDate, "timeSpent": process_time})
    else:
        data["sessions"][-1]["timeSpent"] = process_time

    with open("file.json", "w") as f:
        json.dump(data, f, indent=4)
        # f.write(str({"date": currentDate, "timeSpent":process_time}))
        # f.write("REALLY IMPORTANT DATA")
    sys.exit(0)

if __name__ == "__main__":
    currentDate = datetime.datetime.now().strftime("%d/%m/%y")

    # schedule_rollover()
    # grab the json data
    with open("file.json", "r") as file:
        data = json.load(file)
    
    if data["sessions"][-1]["date"] == currentDate:
        # grab that data
        newDate = False
        process_time = data["sessions"][-1]["timeSpent"]
    else:
        newDate = True

    signal.signal(signal.SIGINT, on_exit) # CTRL C
    signal.signal(signal.SIGTERM, on_exit) # Terminate
    print(currentDate)

    while True:
        record_time()
        print(process_time)

