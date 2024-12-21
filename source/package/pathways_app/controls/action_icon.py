import flet as ft
import theme

from adaptation_pathways.app.model.action import Action


class ActionIcon(ft.Container):
    def __init__(self, action: Action, display_tooltip=True, size=36):
        self.icon = ft.Icon(action.icon, size=(size * 0.5), color=action.color)
        self.ring = ft.Icon(
            ft.icons.CIRCLE_OUTLINED,
            size=size,
            color=action.color,
            tooltip=(
                ft.Tooltip(
                    action.name,
                    bgcolor=action.color,
                    text_style=theme.text.action_tooltip,
                    # vertical_offset=size * 0.75,
                )
                if display_tooltip
                else None
            ),
        )
        super().__init__(
            content=ft.Stack(
                controls=[self.icon, self.ring],
                alignment=ft.alignment.center,
            ),
        )

    def update_action(self, action: Action):
        self.icon.name = action.icon
        self.icon.color = action.color
        self.ring.color = action.color
        self.update()
