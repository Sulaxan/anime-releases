from typing import Any, Callable


def set_or_del(field, field_name, dictionary, val_func: Callable[[], Any]):
    if field:
        dictionary[field_name] = val_func()
    else:
        del dictionary[field_name]


def del_if_none(field, field_name, dictionary):
    if not field:
        del dictionary[field_name]