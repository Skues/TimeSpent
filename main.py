# Camel Case < Snake Case
from win32gui import GetForegroundWindow
import psutil
import time
import win32process
from datetime import timedelta, datetime

import signal
import sys
import json
import schedule

# Global Vars
process_time={} 
timestamp = {}
currentDate = datetime.now().strftime("%d/%m/%y")

def reset_day():
    global currentDate, process_time, newDate
    newDate= True
    print("RESETTING THE DAY")
    print(currentDate)
    save_data()
    date = datetime.strptime(currentDate, "%d/%m/%y")
    currentDate = (date + timedelta(days=1)).strftime("%d/%m/%y")
    print(currentDate)
    process_time = {}

def save_data():
    if newDate:
        data["sessions"].append({"date": currentDate, "timeSpent": process_time})
    else:
        data["sessions"][-1]["timeSpent"] = process_time

    with open("file.json", "w") as f:
        json.dump(data, f, indent=4)




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
    save_data()
    sys.exit(0)

if __name__ == "__main__":
    schedule.every().day.at("00:00").do(reset_day)
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
        schedule.run_pending()
        record_time()

        print(process_time)
        counter += 1
        schedule.every(10).seconds.do()


def writeData(filename, mode, data):
    with open(filename, mode) as f:
        if ".json" in filename:
            json.dump(data, f, indent=4)
        else:
            f.write(data)


schedule.every().day().at("00:00").do(reset_day)