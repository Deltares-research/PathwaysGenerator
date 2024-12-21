import flet as ft
import theme

from adaptation_pathways.app.model import PathwaysProject


class MenuBar(ft.Container):
    def __init__(self, project: PathwaysProject):
        super().__init__(
            content=ft.Stack(
                [
                    ft.Row(
                        [
                            ft.Image(theme.icon),
                            ft.Text("PATHWAYS\nGENERATOR", style=theme.text.logo),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                bgcolor=theme.colors.primary_medium,
                                border_radius=theme.variables.small_radius,
                                alignment=ft.alignment.center,
                                padding=ft.padding.symmetric(0, 15),
                                width=300,
                                content=ft.Stack(
                                    [
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    project.name,
                                                    color=theme.colors.true_white,
                                                ),
                                                ft.Text(
                                                    project.organization,
                                                    text_align=ft.TextAlign.CENTER,
                                                    color=theme.colors.true_white,
                                                ),
                                            ],
                                            spacing=0,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        )
                                    ]
                                ),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            ),
            height=50,
            padding=ft.padding.symmetric(4, 5),
            margin=0,
            bgcolor=theme.colors.primary_dark,
            border_radius=ft.border_radius.only(top_left=0, top_right=0),
            border=ft.border.only(
                bottom=ft.border.BorderSide(1, theme.colors.primary_darker)
            ),
        )
