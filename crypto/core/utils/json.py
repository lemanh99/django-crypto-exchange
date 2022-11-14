import json


def save_data_file_json(file_name, data):
    with open(file_name, "w", encoding='utf-8') as file:
        json.dump(data, fp=file, ensure_ascii=False, indent=4)


def get_data_file_json(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)

    return data
