import flet as ft
import theme


class Panel(ft.Container):
    def __init__(self, content=None, padding=0):
        super().__init__(
            expand=True,
            margin=0,
            padding=ft.padding.symmetric(padding, padding),
            bgcolor=theme.colors.primary_white,
            border=ft.border.all(1, theme.colors.primary_light),
            border_radius=theme.variables.small_radius,
            content=content,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        # [
        #     ft.Container(
        #         content,
        #         bgcolor = theme.colors.primary_white,
        #         border = ft.border.all(1, theme.colors.primary_light),
        #         border_radius = theme.variables.small_radius,
        #         margin=0,
        #         padding=theme.variables.panel_spacing,
        #         expand=1,
        #         left=0,
        #         right=0,
        #         top=0,
        #         bottom=0
        #     )
        # ]
