from typing import Callable

import flet as ft
import theme
from controls.editable_cell import EditableCell
from controls.metric_value import FloatInputFilter
from controls.styled_dropdown import StyledDropdown

from adaptation_pathways.app.model.action import MetricEffect
from adaptation_pathways.app.model.metric import Metric, MetricOperation


class MetricEffectCell(EditableCell):
    def __init__(
        self,
        metric: Metric,
        effect: MetricEffect,
        on_finished_editing: Callable[["MetricEffectCell"], None] | None = None,
    ):
        self.metric = metric
        self.effect = effect

        self.operation_label = ft.Text("", style=theme.text.normal)
        self.value_label = ft.Text("", style=theme.text.normal)

        self.display_content = self.value_label
        self.update_display()

        self.dropdown_focused = False
        self.input_focused = False

        def on_input_blurred(_):
            if not self.input_focused and not self.dropdown_focused:
                self.toggle_editing(_)

        self.operation_dropdown = StyledDropdown(
            "",
            [
                ft.dropdown.Option(key=operation, text=operation.value.upper())
                for operation in MetricOperation
            ],
            text_style=theme.text.normal,
            width=70,
        )

        def on_dropdown_focused(_):
            self.dropdown_focused = True

        def on_dropdown_blurred(_):
            self.dropdown_focused = False
            on_input_blurred(_)

        self.operation_dropdown.on_focus = on_dropdown_focused
        self.operation_dropdown.on_blur = on_dropdown_blurred

        self.value_input = ft.TextField(
            dense=True,
            enable_suggestions=False,
            value="",
            input_filter=FloatInputFilter(),
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=theme.colors.true_white,
            border_color=theme.colors.primary_medium,
            focused_border_color=theme.colors.primary_light,
            cursor_color=theme.colors.primary_medium,
            text_style=theme.text.textfield,
            prefix_style=theme.text.textfield_symbol,
            suffix_style=theme.text.textfield_symbol,
            text_align=ft.TextAlign.RIGHT,
            width=70,
            content_padding=ft.padding.symmetric(4, 6),
        )

        def on_value_input_focused():
            self.input_focused = True

        def on_value_input_blurred(_):
            self.input_focused = False
            on_input_blurred(_)

        self.value_input.on_focus = on_value_input_focused
        self.value_input.on_blur = on_value_input_blurred

        self.input_content = self.value_input
        self.update_input()

        def finished_editing(_):
            self.effect.operation = self.operation_dropdown.key
            self.effect.value = float(self.value_input.value)
            if on_finished_editing is not None:
                on_finished_editing(self)

        super().__init__(
            self.display_content,
            self.input_content,
            on_finished_editing=finished_editing,
        )

    def update_display(self):
        self.operation_label.value = str(self.effect.operation.value).upper()
        self.value_label.value = self.metric.unit.format(self.effect.value)

    def update_input(self):
        self.operation_dropdown.key = self.effect.operation
        self.operation_dropdown.value = self.effect.operation

        symbol = self.metric.unit.get_symbol(self.effect.value)

        if self.metric.unit.place_after_value:
            self.input_content.prefix_text = None
            self.input_content.suffix_text = symbol
        else:
            self.input_content.prefix_text = symbol
            self.input_content.suffix_text = None

        self.value_input.value = self.effect.value
