import flet as ft
import theme
from controls.header import SectionHeader


class TabbedPanel(ft.Column):
    selected_index: int = 0
    tab_buttons: list[ft.TextButton]
    content: ft.Container

    def __init__(
        self, tabs: list[tuple[SectionHeader, ft.Control]], selected_index: int
    ):
        def get_tab_bgcolor(index: int):
            if self.selected_index == index:
                return theme.colors.primary_white
            return theme.colors.primary_white

        def get_opacity(index: int):
            return 1 if self.selected_index == index else 0.5

        def on_click(e):
            self.selected_index = self.tab_buttons.index(e.control)

            for [index, tab] in enumerate(self.tab_buttons):
                tab.content.bgcolor = get_tab_bgcolor(index)
                tab.content.opacity = get_opacity(index)
                tab.content.update()

            self.content.content = tabs[self.selected_index][1]
            self.content.update()

        super().__init__(
            expand=True, spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        )

        self.selected_index = selected_index

        self.tab_buttons = [
            ft.TextButton(
                expand=True,
                content=ft.Container(
                    expand=True,
                    content=tab[0],
                    padding=10,
                    bgcolor=get_tab_bgcolor(index),
                    opacity=get_opacity(index),
                    border_radius=ft.border_radius.only(
                        top_left=theme.variables.small_radius,
                        top_right=theme.variables.small_radius,
                    ),
                    border=ft.border.only(
                        left=ft.BorderSide(1, theme.colors.primary_light),
                        right=ft.BorderSide(1, theme.colors.primary_light),
                        top=ft.BorderSide(1, theme.colors.primary_light),
                    ),
                ),
                style=ft.ButtonStyle(padding=0),
                on_click=on_click,
            )
            for [index, tab] in enumerate(tabs)
        ]

        self.content = ft.Container(
            expand=True,
            content=tabs[selected_index][1],
            margin=0,
            padding=theme.variables.panel_padding,
            bgcolor=theme.colors.primary_white,
            border=ft.border.only(
                left=ft.BorderSide(1, theme.colors.primary_light),
                right=ft.BorderSide(1, theme.colors.primary_light),
                bottom=ft.BorderSide(1, theme.colors.primary_light),
            ),
            border_radius=ft.border_radius.only(
                bottom_left=theme.variables.small_radius,
                bottom_right=theme.variables.small_radius,
            ),
        )

        self.controls = [
            ft.Row(
                controls=self.tab_buttons,
                spacing=3,
            ),
            self.content,
        ]
