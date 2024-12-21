from typing import Callable

import flet as ft
from controls.editable_cell import EditableTextCell
from controls.header import SmallHeader
from controls.styled_button import StyledButton
from controls.styled_table import StyledTable
from controls.unit_cell import MetricUnitCell

from adaptation_pathways.app.model.metric import Metric
from adaptation_pathways.app.model.pathways_project import PathwaysProject


class MetricsPanel(ft.Column):
    def __init__(self, project: PathwaysProject):
        super().__init__()

        self.project = project
        self.expand = False
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        self.spacing = 40

        self.conditions_table = StyledTable(
            columns=[
                ft.DataColumn(label=ft.Text("Name")),
                ft.DataColumn(label=ft.Text("Unit")),
            ],
            rows=[],
            show_checkboxes=True,
        )

        self.criteria_table = StyledTable(
            columns=[
                ft.DataColumn(label=ft.Text("Name")),
                ft.DataColumn(label=ft.Text("Unit")),
            ],
            rows=[],
            show_checkboxes=True,
        )

        self.delete_condition_button = StyledButton(
            "Delete", ft.icons.DELETE, self.on_delete_conditions
        )
        self.delete_criteria_button = StyledButton(
            "Delete", ft.icons.DELETE, self.on_delete_criteria
        )

        self.update_metrics()

        self.controls = [
            ft.Column(
                expand=False,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        expand=False,
                        controls=[
                            SmallHeader("Conditions"),
                            ft.Container(expand=True),
                            self.delete_condition_button,
                            StyledButton(
                                "New",
                                icon=ft.icons.ADD_CIRCLE_OUTLINE,
                                on_click=self.on_new_condition,
                            ),
                        ],
                    ),
                    self.conditions_table,
                ],
            ),
            ft.Column(
                expand=False,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        expand=False,
                        controls=[
                            SmallHeader("Criteria"),
                            ft.Container(expand=True),
                            self.delete_criteria_button,
                            StyledButton(
                                text="New",
                                icon=ft.icons.ADD_CIRCLE_OUTLINE,
                                on_click=self.on_new_criteria,
                            ),
                        ],
                    ),
                    self.criteria_table,
                ],
            ),
        ]

    def redraw(self):
        self.update_metrics()
        self.update()

    def on_metric_updated(self, _):
        print(self)
        self.project.notify_conditions_changed()

    def on_condition_selected(self, metric: Metric):
        if metric.id in self.project.selected_condition_ids:
            self.project.selected_condition_ids.remove(metric.id)
        else:
            self.project.selected_condition_ids.add(metric.id)

        self.redraw()

    def on_criteria_selected(self, metric: Metric):
        if metric.id in self.project.selected_criteria_ids:
            self.project.selected_criteria_ids.remove(metric.id)
        else:
            self.project.selected_criteria_ids.add(metric.id)

        self.redraw()

    def on_new_condition(self, _):
        metric = self.project.create_condition()
        self.project.update_pathway_values(metric.id)
        self.project.notify_conditions_changed()

    def on_delete_conditions(self, _):
        for metric_id in self.project.selected_condition_ids:
            self.project.delete_condition(metric_id)
        self.project.notify_conditions_changed()

    def on_new_criteria(self, _):
        metric = self.project.create_criteria()
        self.project.update_pathway_values(metric.id)
        self.project.notify_criteria_changed()

    def on_delete_criteria(self, _):
        for metric_id in self.project.selected_criteria_ids:
            self.project.delete_criteria(metric_id)
        self.project.notify_criteria_changed()

    def get_metric_row(
        self,
        metric: Metric,
        selected_ids: set[str],
        on_metric_selected: Callable[[Metric], None],
    ) -> ft.DataRow:
        row = ft.DataRow(
            [
                EditableTextCell(metric, "name", self.on_metric_updated),
                MetricUnitCell(metric, self.on_metric_updated),
            ],
            selected=metric.id in selected_ids,
        )
        row.on_select_changed = lambda e: on_metric_selected(metric)
        return row

    def update_metrics(self):
        self.conditions_table.set_rows(
            [
                self.get_metric_row(
                    metric,
                    self.project.selected_condition_ids,
                    self.on_condition_selected,
                )
                for metric in self.project.sorted_conditions
            ]
        )
        has_selected_conditions = len(self.project.selected_condition_ids) > 0
        self.delete_condition_button.visible = has_selected_conditions

        self.criteria_table.set_rows(
            [
                self.get_metric_row(
                    metric,
                    self.project.selected_criteria_ids,
                    self.on_criteria_selected,
                )
                for metric in self.project.sorted_criteria
            ]
        )
        has_selected_criteria = len(self.project.selected_criteria_ids) > 0
        self.delete_criteria_button.visible = has_selected_criteria
