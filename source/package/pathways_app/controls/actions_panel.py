# pylint: disable=too-many-arguments,too-many-instance-attributes
import random

import flet as ft
import theme
from controls.action_icon import ActionIcon
from controls.editable_cell import EditableTextCell
from controls.metric_effect import MetricEffectCell
from controls.metric_value import MetricValueCell
from controls.sortable_header import SortableHeader, SortMode
from controls.styled_button import StyledButton
from controls.styled_table import StyledTable

from adaptation_pathways.app.model.action import Action
from adaptation_pathways.app.model.pathways_project import PathwaysProject
from adaptation_pathways.app.model.sorting import SortTarget


class ActionsPanel(ft.Column):
    def __init__(self, project: PathwaysProject):
        super().__init__(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=40,
            scroll=ft.ScrollMode.AUTO,
        )

        self.project = project

        self.action_table = StyledTable(
            columns=[], rows=[], row_height=42, show_checkboxes=True
        )

        self.delete_action_button = StyledButton(
            "Delete",
            icon=ft.icons.DELETE,
            on_click=self.on_delete_actions,
        )

        self.update_table()

        self.controls = [
            ft.Column(
                expand=False,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        expand=True,
                        controls=[
                            ft.Container(expand=True),
                            self.delete_action_button,
                            StyledButton(
                                "New",
                                icon=ft.icons.ADD_CIRCLE_OUTLINE,
                                on_click=self.on_new_action,
                            ),
                        ],
                    ),
                    self.action_table,
                ],
            ),
        ]

    def redraw(self):
        self.update_table()
        # self.update()

    def on_name_edited(self, _):
        self.project.notify_actions_changed()
        self.update()

    def on_cell_edited(self, cell: MetricValueCell):
        self.project.update_pathway_values(cell.metric.id)
        self.project.notify_actions_changed()
        self.update()

    def on_action_selected(self, action: Action):
        if action.id in self.project.selected_action_ids:
            self.project.selected_action_ids.remove(action.id)
        else:
            self.project.selected_action_ids.add(action.id)
        self.redraw()
        self.update()

    def on_sort_actions(self, header: SortableHeader):
        if header.sort_mode == SortMode.NONE:
            self.project.action_sorting.target = SortTarget.NONE
            self.project.action_sorting.sort_key = None
            self.project.action_sorting.ascending = True
        else:
            self.project.action_sorting.target = (
                SortTarget.ATTRIBUTE if header.sort_key == "name" else SortTarget.METRIC
            )
            self.project.action_sorting.sort_key = header.sort_key
            self.project.action_sorting.ascending = (
                header.sort_mode == SortMode.ASCENDING
            )

        self.project.sort_actions()
        self.project.notify_actions_changed()
        self.update()

    def on_delete_actions(self, _):
        self.project.delete_selected_actions()
        self.project.notify_actions_changed()
        self.update()

    def on_new_action(self, _):
        self.project.create_action(
            random.choice(theme.action_colors),
            random.choice(theme.action_icons),
        )
        self.project.notify_actions_changed()
        self.update()

    def update_table(self):
        sort_mode = SortableHeader.get_sort_mode(self.project.action_sorting)
        sort_key = self.project.action_sorting.sort_key

        sortable_headers = [
            SortableHeader(
                sort_key="name",
                name="Name",
                sort_mode=SortMode.NONE if sort_key != "name" else sort_mode,
                on_sort=self.on_sort_actions,
            ),
            *(
                SortableHeader(
                    sort_key=metric.id,
                    name=metric.name,
                    sort_mode=SortMode.NONE if sort_key is not metric.id else sort_mode,
                    on_sort=self.on_sort_actions,
                )
                for metric in self.project.all_metrics()
            ),
        ]

        columns = [
            ft.DataColumn(
                label=ft.Text("Icon", expand=True),
            ),
            *(
                ft.DataColumn(label=header, numeric=header.sort_key != "name")
                for header in sortable_headers
            ),
        ]
        self.action_table.set_columns(columns)

        self.update_rows()
        self.delete_action_button.visible = len(self.project.selected_action_ids) > 0

    def create_icon_editor(self, action: Action):
        def on_color_picked(color: str):
            action.color = color
            action_icon.update_action(action)
            self.project.notify_action_color_changed()

        def on_icon_picked(icon: str):
            action.icon = icon
            action_icon.update_action(action)
            self.project.notify_action_color_changed()

        def on_editor_closed(_):
            self.project.notify_actions_changed()

        def update_items():
            action_button.items = [
                ft.PopupMenuItem(
                    content=ft.GridView(
                        spacing=4,
                        width=200,
                        runs_count=4,
                        padding=ft.padding.symmetric(4, 6),
                        child_aspect_ratio=1.0,
                        controls=[
                            ft.Container(
                                bgcolor=color,
                                border=ft.border.all(
                                    2,
                                    (
                                        theme.colors.primary_medium
                                        if action.color == color
                                        else theme.colors.primary_lightest
                                    ),
                                ),
                                on_click=lambda e, c=color: on_color_picked(c),
                                width=10,
                                height=10,
                            )
                            for color in theme.action_colors
                        ],
                    )
                ),
                ft.PopupMenuItem(
                    content=ft.GridView(
                        expand=True,
                        runs_count=5,
                        padding=ft.padding.symmetric(12, 6),
                        controls=[
                            ft.Container(
                                ft.Icon(icon),
                                on_click=lambda e, i=icon: on_icon_picked(i),
                            )
                            for icon in theme.action_icons
                        ],
                        spacing=4,
                    )
                ),
            ]

        action_icon = ActionIcon(action)

        action_button = ft.PopupMenuButton(
            action_icon,
            items=[],
            bgcolor=theme.colors.off_white,
            menu_position=ft.PopupMenuPosition.UNDER,
            on_cancel=on_editor_closed,
        )
        update_items()
        return action_button

    def update_rows(self):
        rows = []

        for action in self.project.sorted_actions:
            metric_cells = []
            for metric in self.project.all_metrics():
                effect = action.metric_data[metric.id]
                metric_cells.append(
                    MetricEffectCell(
                        metric, effect, on_finished_editing=self.on_cell_edited
                    )
                )

            rows.append(
                ft.DataRow(
                    [
                        ft.DataCell(self.create_icon_editor(action)),
                        EditableTextCell(action, "name", self.on_name_edited),
                        *metric_cells,
                    ],
                    selected=action.id in self.project.selected_action_ids,
                    on_select_changed=lambda _, a=action: self.on_action_selected(a),
                )
            )

        self.action_table.set_rows(rows)
