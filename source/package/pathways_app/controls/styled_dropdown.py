# pylint: disable=too-many-arguments
import flet as ft
import theme
from utils import index_of_first


class StyledDropdown(ft.Dropdown):
    def __init__(
        self,
        value: str,
        options: list[ft.dropdown.Option],
        option_icons: list[str] | None = None,
        width: ft.OptionalNumber = None,
        height: ft.OptionalNumber = 28,
        text_style: ft.TextStyle | None = None,
        on_change=None,
        on_blur=None,
    ):
        super().__init__(
            value=value,
            text_style=text_style,
            expand=False,
            options=options,
            width=width,
            bgcolor=theme.colors.true_white,
            content_padding=ft.padding.symmetric(4, 8),
            padding=0,
            height=height,
            border_color=theme.colors.primary_dark,
            icon_enabled_color=theme.colors.primary_dark,
            on_blur=on_blur,
        )

        def update_icon():
            if option_icons is None:
                return

            option_index = index_of_first(options, lambda el: el.key == self.value)
            if option_index is not None:
                self.prefix = ft.Row(
                    spacing=5,
                    controls=[
                        ft.Icon(
                            option_icons[option_index],
                            color=theme.colors.primary_dark,
                            expand=False,
                        ),
                        ft.Text(self.value, style=text_style),
                    ],
                )

        def on_value_changed(e):
            update_icon()
            self.update()

            if on_change is not None:
                on_change(e)

        self.prefix = None
        update_icon()
        self.on_change = on_value_changed
