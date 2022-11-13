def get_dict_in_list(key, value, my_dictlist):
    for entry in my_dictlist:
        if entry[key] == value:
            return entry
    return {}
