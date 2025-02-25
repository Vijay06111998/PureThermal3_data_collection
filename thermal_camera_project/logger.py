import json
import datetime

def log_data(objects):
    data_entry = {"timestamp": datetime.datetime.utcnow().isoformat(), "objects": objects}
    try:
        with open("thermal_data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    
    data.append(data_entry)
    with open("thermal_data.json", "w") as file:
        json.dump(data, file, indent=4)