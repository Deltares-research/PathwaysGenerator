# pylint: disable=too-many-arguments
import flet as ft
from src import theme


class SectionHeader(ft.Container):
    def __init__(
        self,
        icon: str | None = None,
        text: str | None = None,
        size=16,
        expand=False,
        color=theme.colors.primary_dark,
        padding=ft.padding.symmetric(6, 0),
        border_radius=0,
        border: ft.Border | None = None,
        bgcolor: str | None = None,
    ):
        super().__init__(
            height=(size + padding.top + padding.bottom),
            padding=padding,
            expand=expand,
            bgcolor=bgcolor,
            border_radius=border_radius,
            border=border,
        )

        self.clip_behavior = ft.ClipBehavior.NONE

        header_text_style = ft.TextStyle(
            size=size,
            height=1,
            color=color,
            weight=ft.FontWeight.W_600,
        )

        self.icon = ft.Icon(icon, size=size, color=color)
        self.icon.visible = icon is not None

        self.text = ft.Text(text, style=header_text_style)
        self.text.visible = text is not None

        self.content = ft.Row(
            expand=expand,
            controls=[
                self.icon,
                self.text,
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )


class SmallHeader(ft.Text):
    def __init__(self, text: str):
        super().__init__(value=text.upper(), style=ft.TextStyle(size=12))
