from abc import ABC
from typing import Callable

import flet as ft
import theme
from pyparsing import abstractmethod


class EditableCell(ft.DataCell, ABC):
    def __init__(
        self,
        display_control: ft.Control,
        edit_control: ft.Control,
        is_calculated=False,
        is_editing=False,
        on_finished_editing: Callable[["EditableCell"], None] | None = None,
    ):
        self.display_content = display_control
        self.input_content = edit_control
        self.is_calculated = is_calculated
        self.is_editing = is_editing
        self.on_finished_editing = on_finished_editing

        self.display_content.visible = not self.is_editing
        self.input_content.visible = self.is_editing

        self.cell_content = ft.Container(
            expand=True,
            content=ft.Stack([self.display_content, self.input_content]),
            on_click=self.toggle_editing,
        )

        self.update_bg()

        super().__init__(content=self.cell_content)

    def toggle_editing(self, _):
        self.is_editing = not self.is_editing

        if self.is_editing:
            self.update_input()
        else:
            self.update_display()

        self.display_content.visible = not self.is_editing
        self.input_content.visible = self.is_editing

        self.update_bg()
        self.update()

        if self.is_editing:
            self.input_content.focus()
        else:
            if self.on_finished_editing is not None:
                self.on_finished_editing(self)

    def update_bg(self):
        self.cell_content.bgcolor = (
            theme.colors.calculated_bg
            if self.is_calculated and not self.is_editing
            else None
        )

    def set_calculated(self, is_calculated):
        self.is_calculated = is_calculated
        self.update_bg()
        self.update()

    @abstractmethod
    def update_display(self):
        pass

    @abstractmethod
    def update_input(self):
        pass


class EditableTextCell(EditableCell):
    def __init__(self, source: object, value_attribute: str, on_finished_editing=None):
        self.source = source
        self.value_attribute = value_attribute

        self.display_content = ft.Text(self.value, expand=True)
        self.input_content = ft.TextField(
            dense=True,
            enable_suggestions=False,
            value=self.value,
            keyboard_type=ft.KeyboardType.TEXT,
            bgcolor=theme.colors.true_white,
            border_color=theme.colors.primary_medium,
            focused_border_color=theme.colors.primary_light,
            cursor_color=theme.colors.primary_medium,
            text_style=theme.text.textfield,
            prefix_style=theme.text.textfield_symbol,
            suffix_style=theme.text.textfield_symbol,
            expand=True,
            content_padding=ft.padding.symmetric(4, 6),
            on_blur=self.toggle_editing,
        )

        def on_finished_editing_internal(_):
            self.value = self.input_content.value
            if on_finished_editing is not None:
                on_finished_editing(self)

        super().__init__(
            self.display_content,
            self.input_content,
            on_finished_editing=on_finished_editing_internal,
        )

    @property
    def value(self) -> str:
        return getattr(self.source, self.value_attribute)

    @value.setter
    def value(self, value: str):
        setattr(self.source, self.value_attribute, value)

    def update_input(self):
        self.input_content.value = self.display_content.value

    def update_display(self):
        self.display_content.value = self.input_content.value
