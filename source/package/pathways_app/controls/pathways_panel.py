import flet as ft
import theme
from controls.action_icon import ActionIcon
from controls.header import SectionHeader
from controls.metric_value import MetricValueCell
from controls.sortable_header import SortableHeader, SortMode
from controls.styled_button import StyledButton
from controls.styled_table import StyledTable

from adaptation_pathways.app.model.pathway import Pathway
from adaptation_pathways.app.model.pathways_project import PathwaysProject
from adaptation_pathways.app.model.sorting import SortTarget


class PathwaysPanel(ft.Column):
    def __init__(self, project: PathwaysProject):
        self.project = project

        self.rows_by_pathway: dict[Pathway, ft.DataRow] = {}

        self.pathway_table = StyledTable(columns=[], rows=[], show_checkboxes=True)
        self.delete_pathways_button = StyledButton(
            "Delete", ft.icons.DELETE, self.on_delete_pathways
        )
        self.update_table()

        super().__init__(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Column(
                    expand=False,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        ft.Row(
                            [
                                SectionHeader(
                                    ft.icons.ACCOUNT_TREE_OUTLINED, "Pathways"
                                ),
                                ft.Container(expand=True),
                                self.delete_pathways_button,
                            ],
                            spacing=15,
                        ),
                        self.pathway_table,
                    ],
                )
            ],
        )

    def redraw(self):
        self.update_table()
        self.update()

    def on_delete_pathways(self, _):
        self.project.delete_selected_pathways()
        self.project.notify_pathways_changed()

    def on_sort_table(self, header: SortableHeader):
        if header.sort_mode is SortMode.NONE:
            self.project.pathway_sorting.target = SortTarget.NONE
            self.project.pathway_sorting.sort_key = None
            self.project.pathway_sorting.ascending = True
        else:
            self.project.pathway_sorting.target = SortTarget.METRIC
            self.project.pathway_sorting.sort_key = header.sort_key
            self.project.pathway_sorting.ascending = (
                header.sort_mode == SortMode.ASCENDING
            )

        self.project.sort_pathways()
        self.project.notify_pathways_changed()

    def update_table(self):
        sorting = self.project.pathway_sorting
        sort_mode = SortableHeader.get_sort_mode(sorting)

        self.delete_pathways_button.visible = (
            len(self.project.selected_pathway_ids) > 0
            and not self.project.root_pathway_id in self.project.selected_pathway_ids
        )

        self.pathway_table.set_columns(
            [
                ft.DataColumn(ft.Text("Pathway")),
                *(
                    ft.DataColumn(
                        SortableHeader(
                            metric.id,
                            metric.name,
                            sort_mode=(
                                SortMode.NONE
                                if sorting.sort_key is not metric.id
                                else sort_mode
                            ),
                            on_sort=self.on_sort_table,
                        ),
                        numeric=True,
                    )
                    for metric in self.project.all_metrics()
                ),
            ]
        )

        rows = []

        self.rows_by_pathway = {}
        for pathway in self.project.sorted_pathways:
            ancestors = self.project.get_ancestors_and_self(pathway)
            path = [*reversed([*ancestors])]
            # if len(path) > 1:
            #     path = path[1:]
            row = self.get_pathway_row(pathway, path)
            if pathway.id == self.project.root_pathway_id:
                row.on_select_changed = None
            self.rows_by_pathway[pathway] = row
            rows.append(row)

        self.pathway_table.set_rows(rows)
        return rows

    def on_metric_value_edited(self, cell: MetricValueCell):
        self.project.update_pathway_values(cell.metric.id)
        self.project.sort_pathways()
        self.project.notify_pathways_changed()

    def get_pathway_row(self, pathway: Pathway, ancestors: list[Pathway]):
        children = [*self.project.get_children(pathway.id)]
        pathway_action = self.project.get_action(pathway.action_id)

        unused_action_ids = [
            action_id
            for action_id in self.project.action_sorting.sorted_ids
            if not any(ancestor.action_id == action_id for ancestor in ancestors)
            and not any(child.action_id == action_id for child in children)
        ]

        row_controls = [
            ActionIcon(self.project.get_action(ancestor.action_id), size=26)
            for ancestor in ancestors
        ]

        if pathway.parent_id is None:
            row_controls.append(ft.Text("  Current  ", color=pathway_action.color))

        if len(unused_action_ids) > 0:
            row_controls.append(
                ft.PopupMenuButton(
                    ft.Icon(
                        ft.icons.ADD_CIRCLE_OUTLINE,
                        size=20,
                        color=theme.colors.primary_lightest,
                    ),
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row(
                                [
                                    ActionIcon(
                                        action,
                                        display_tooltip=False,
                                    ),
                                    ft.Text(
                                        action.name,
                                        style=theme.text.normal,
                                    ),
                                ]
                            ),
                            on_click=lambda e, action_id=action_id: self.extend_pathway(
                                pathway, action_id
                            ),
                        )
                        for action_id in unused_action_ids
                        for action in [self.project.get_action(action_id)]
                    ],
                    tooltip=ft.Tooltip(
                        "Add",
                        bgcolor=theme.colors.primary_white,
                    ),
                    bgcolor=theme.colors.off_white,
                    menu_position=ft.PopupMenuPosition.UNDER,
                ),
            )

        row = ft.DataRow(
            [
                ft.DataCell(
                    ft.Container(
                        expand=True,
                        content=ft.Row(
                            spacing=0,
                            controls=row_controls,
                        ),
                    ),
                ),
                *(
                    MetricValueCell(
                        metric,
                        pathway.metric_data[metric.id],
                        on_finished_editing=self.on_metric_value_edited,
                    )
                    for metric in self.project.all_metrics()
                ),
            ],
            selected=pathway.id in self.project.selected_pathway_ids,
        )

        if pathway.parent_id is None:
            row.color = "#EEEEEE"

        def on_select_changed(_):
            if pathway.id in self.project.selected_pathway_ids:
                self.project.selected_pathway_ids.remove(pathway.id)
            else:
                self.project.selected_pathway_ids.add(pathway.id)

            self.project.notify_pathways_changed()

        row.on_select_changed = on_select_changed
        return row

    def extend_pathway(self, pathway: Pathway, action_id: str):
        self.project.create_pathway(action_id, pathway.id)
        self.project.sort_pathways()
        self.project.notify_pathways_changed()
