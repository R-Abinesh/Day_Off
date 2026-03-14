import json

def load_attractions(file_path:str):
    with open(file_path,'r') as f:
        data = json.load(f)
    return data

def load_restaurants(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data