def get_dict_in_list(key, value, my_dictlist):
    for entry in my_dictlist:
        if entry[key] == value:
            return entry
    return {}


def get_list_dict_in_list_by_value(key, value, my_dictlist):
    list_item = []
    for entry in my_dictlist:
        if entry[key] == value:
            list_item.append(entry)
    return list_item


def get_list_in_dict_by_key(key, my_dictlist):
    return [entry[key] for entry in my_dictlist]


def get_unique_list_of_dict(my_dictlist: list):
    return list(map(dict, set(tuple(sorted(entry.items())) for entry in my_dictlist)))
