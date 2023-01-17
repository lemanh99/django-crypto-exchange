from operator import itemgetter


def list_to_str(lis):
    return "\n".join(lis)


def list_to_str_with_idx(lis):
    return "\n".join([f"{idx + 1}: {l}" for idx, l in enumerate(lis)])


def sort_list_of_dict(my_list, key_sort, reverse=True):
    return sorted(my_list, key=itemgetter(key_sort), reverse=reverse)
