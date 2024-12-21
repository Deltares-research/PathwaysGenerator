import flet as ft
import theme


class StyledButton(ft.FilledButton):
    def __init__(
        self,
        text: str | None = None,
        icon: str | None = None,
        on_click=None,
    ):
        super().__init__(
            style=theme.buttons.primary,
            height=28,
            on_click=on_click,
        )

        row = ft.Row(
            controls=[], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        if icon is not None:
            row.controls.append(ft.Icon(icon, color=theme.colors.true_white, size=16))

        if text is not None:
            row.controls.append(ft.Text(text, style=theme.buttons.primary))

        self.content = ft.Container(content=row, padding=ft.padding.symmetric(4, 8))
