import json

from waterproject.wlib.Device import Device


log_file = "log.csv"

def read_configuration(file_path="config.json"):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    data_devices = data['devices']
    project_name = data['project_name']
    devices = [Device(device['name'], device['pin'], device['location']) for device in data_devices]
    return devices,project_name