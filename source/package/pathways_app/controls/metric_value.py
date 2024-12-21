import flet as ft
import theme
from controls.editable_cell import EditableCell

from adaptation_pathways.app.model.metric import Metric, MetricValue


class FloatInputFilter(ft.InputFilter):
    def __init__(self):
        super().__init__(
            regex_string=r"^$|^[-+]?\d*(\.\d*)?$", allow=True, replacement_string=""
        )


class MetricValueCell(EditableCell):
    def __init__(self, metric: Metric, value: MetricValue, on_finished_editing=None):
        self.metric = metric
        self.value = value

        self.display_content = ft.Text("")
        self.update_display()

        def on_edited(_):
            self.value.value = float(self.input_content.value)
            self.value.is_estimate = False
            self.set_calculated(False)
            if on_finished_editing is not None:
                on_finished_editing(self)

        self.input_content = ft.TextField(
            dense=True,
            enable_suggestions=False,
            value=value.value,
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
            expand=True,
            content_padding=ft.padding.symmetric(4, 6),
            on_blur=self.toggle_editing,
        )
        self.update_input()

        super().__init__(
            self.display_content,
            self.input_content,
            is_calculated=value.is_estimate,
            on_finished_editing=on_edited,
        )

    def update_display(self):
        self.display_content.value = self.metric.unit.format(self.value.value)

    def update_input(self):
        symbol = self.metric.unit.get_symbol(self.value.value)

        if self.metric.unit.place_after_value:
            self.input_content.prefix_text = None
            self.input_content.suffix_text = symbol
        else:
            self.input_content.prefix_text = symbol
            self.input_content.suffix_text = None
