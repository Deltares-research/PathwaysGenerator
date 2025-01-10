from enum import Enum

import flet as ft
import theme

from adaptation_pathways.app.model.sorting import SortingInfo, SortTarget


class SortMode(Enum):
    NONE = 0
    UNSORTED = 1
    ASCENDING = 2
    DESCENDING = 3

    def get_icon(self):
        match self:
            case SortMode.ASCENDING:
                return ft.icons.KEYBOARD_ARROW_UP
            case SortMode.DESCENDING:
                return ft.icons.KEYBOARD_ARROW_DOWN
            case SortMode.UNSORTED:
                return ft.icons.UNFOLD_MORE
            case _:
                return None


class SortableHeader(ft.Container):
    def __init__(
        self,
        sort_key: str,
        name: str,
        sort_mode: SortMode = SortMode.NONE,
        on_sort=None,
        expand: bool | int | None = True,
        col: int | None = None,
        bgcolor: str | None = None,
        width: int | None = None,
        height: int | None = None,
    ):
        self.sort_key = sort_key
        self.name = name
        self.sort_mode = sort_mode
        self.icon = ft.Icon(sort_mode.get_icon(), size=16)
        self.update_icon()

        super().__init__(
            expand=expand,
            col=col,
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Text(name, expand=True, style=theme.text.table_header),
                    self.icon,
                ],
            ),
            padding=theme.variables.table_cell_padding,
            bgcolor=bgcolor,
            width=width,
            height=height,
        )

        def on_click(_):
            if self.sort_mode == SortMode.NONE:
                pass

            new_sort_mode = (
                SortMode.ASCENDING
                if self.sort_mode == SortMode.UNSORTED
                else (
                    SortMode.DESCENDING
                    if self.sort_mode == SortMode.ASCENDING
                    else SortMode.UNSORTED
                )
            )
            self.set_sort_mode(new_sort_mode)

            if on_sort is not None:
                on_sort(self)

        self.on_click = on_click

    @classmethod
    def get_sort_mode(cls, sort_info: SortingInfo) -> SortMode:
        if sort_info.target is SortTarget.NONE:
            return SortMode.NONE
        return SortMode.ASCENDING if sort_info.ascending else SortMode.DESCENDING

    def set_sort_mode(self, sort_mode: SortMode):
        self.sort_mode = sort_mode
        self.update_icon()
        # self.icon.update()

    def update_icon(self):
        self.icon.name = self.sort_mode.get_icon()
        self.icon.color = (
            theme.colors.primary_lighter
            if self.sort_mode is SortMode.UNSORTED
            else theme.colors.primary_dark
        )
        self.icon.visible = self.sort_mode != SortMode.NONE
