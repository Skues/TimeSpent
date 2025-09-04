# Camel Case < Snake Case
from win32gui import GetForegroundWindow
import psutil
import time
import win32process
import datetime

import signal
import sys
import json

# Global Vars
process_time={} 
timestamp = {}

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
        
def on_exit(signum, frame):
    """
    Runs when the program is closed using CTRL C or Terminated
    """
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
    # grab the json data
    with open("file.json", "r") as file:
        data = json.load(file)
    
    if data["sessions"][-1]["date"] == currentDate:
        # grab that data
        newDate = False
        process_time = data["sessions"][-1]["timeSpent"]
    else:
        newDate = True


    exampleData= {"date": "2025-09-04", "timeSpent":{'WindowsTerminal': 3, 'Discord': 17, 'CMSEngine': 3, 'Code': 4}}

    signal.signal(signal.SIGINT, on_exit) # CTRL C
    signal.signal(signal.SIGTERM, on_exit) # Terminate
    print(currentDate)

    while True:
        record_time()
        print(process_time)

