import json

def init_config():
    try:
        with open('config.json') as config_file:
            return json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Failed to load config.json. Make sure it exists and is valid JSON.")
        return None

config = init_config()
