import json
from json.decoder import JSONDecodeError
from pathlib import Path

def json_load_dict(file : str ) -> dict:
    road = Path(f'db/{file}.json')
    data = {}
    try:
        with open (road) as json_l:
            try:
                data = json.load(json_l)
                return data
            except JSONDecodeError:
                return data
    except OSError:
            with open(road, 'w') as json_s:
                pass
            return data

def json_save_dict(file : str, data : dict):
    road = Path(f'db/{file}.json')
    with open(road, 'w') as json_s:
        json.dump(data, json_s, indent = 2)

def json_load_list(file:str) -> list:
    road = Path(f'db/{file}.json')
    data = []
    try:
        with open (road) as json_l:
            try:
                data = json.load(json_l)
                return data
            except JSONDecodeError:
                return data
    except OSError:
            with open(road, 'w') as json_s:
                pass
            return data

def json_save_list(file : str, data : list):
    road = Path(f'db/{file}.json')
    with open(road, 'w') as json_s:
        json.dump(data, json_s, indent = 2)    


