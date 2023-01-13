import json


def save_data_file_json(file_name, data):
    with open(file_name, "w", encoding='utf-8') as file:
        json.dump(data, fp=file, ensure_ascii=False, indent=4)


def get_data_file_json(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)

    return data


def convert_string_to_json(text: str):
    try:
        return json.loads(text)
    except json.decoder.JSONDecodeError:
        return text


def convert_json_to_string(text: dict):
    try:
        return json.dumps(text)
    except json.decoder.JSONDecodeError:
        return text
