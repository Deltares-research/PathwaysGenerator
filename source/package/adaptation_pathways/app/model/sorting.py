from enum import Enum


class SortTarget(Enum):
    NONE = 0
    ATTRIBUTE = 1
    METRIC = 2


class SortingInfo:
    def __init__(
        self,
        ids: list[str],
        target=SortTarget.NONE,
        sort_key: str | None = None,
        ascending=True,
    ):
        self.sorted_ids = ids
        self.target = target
        self.sort_key = sort_key
        self.ascending = ascending

    def sort_by_id(self):
        self.sorted_ids.sort(reverse=not self.ascending)
