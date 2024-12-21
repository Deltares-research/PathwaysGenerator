from typing import Any, Callable


def index_of_first(element_list: list[Any], pred: Callable[[Any], bool]) -> int | None:
    for index, value in enumerate(element_list):
        if pred(value):
            return index
    return None
