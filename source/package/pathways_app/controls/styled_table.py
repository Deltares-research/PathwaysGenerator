# pylint: disable=too-many-arguments
from typing import Callable

import flet as ft
import theme
from pathways_app.controls.sortable_header import SortableHeader, SortMode


class TableColumn:
    def __init__(
        self,
        label: str,
        key: str | None = None,
        on_sort: Callable[[None], None] | None = None,
        expand: bool | int | None = True,
        width: int | None = None,
        alignment: ft.Alignment | None = ft.alignment.center_left,
    ):

        self.label = label
        self.on_sort = on_sort
        self.expand = expand
        self.key = label if key is None else key
        self.alignment = alignment
        self.width = width


class TableCell:
    def __init__(
        self,
        control: ft.Control,
        sort_value: int | float | None = None,
    ):
        self.control = control
        self.sort_value = sort_value


class StyledTable(ft.Container):
    def __init__(
        self,
        columns: list[TableColumn],
        rows: list[list[TableCell]],
        row_height=36,
        sort_column_index: int | None = None,
        sort_ascending: bool | None = None,
        on_sort: Callable[[int], None] | None = None,
        show_checkboxes=False,
    ):
        super().__init__(
            expand=True,
            # horizontal_margin=0,
            # show_checkbox_column=show_checkboxes,
            # checkbox_horizontal_margin=theme.variables.table_cell_padding.left,
            # columns=columns,
            # rows=rows,
            # bgcolor=theme.colors.true_white,
            # sort_column_index=sort_column_index,
            # sort_ascending=sort_ascending,
            # column_spacing=20,
            # data_row_min_height=0,
            # data_row_max_height=row_height,
            # data_row_color={
            #     ft.ControlState.HOVERED: theme.colors.off_white,
            #     ft.ControlState.FOCUSED: theme.colors.off_white,
            #     ft.ControlState.SELECTED: theme.colors.primary_white,
            #     ft.ControlState.PRESSED: theme.colors.off_white,
            #     ft.ControlState.DRAGGED: theme.colors.off_white,
            #     ft.ControlState.SCROLLED_UNDER: theme.colors.off_white,
            # },
            # divider_thickness=0,
            # horizontal_lines=ft.BorderSide(1, theme.colors.primary_lightest),
            # heading_row_height=30,
            # heading_row_color=theme.colors.primary_lightest,
            # heading_text_style=theme.text.table_header,
            # border=ft.border.all(1, theme.colors.primary_light),
        )

        self.row_height = row_height
        self.sort_column_index = sort_column_index
        self.show_checkboxes = show_checkboxes
        self.on_sort = on_sort
        self.sort_ascending = sort_ascending
        self.selected_row_indices: set[int] = set()
        self.header_row = ft.Container(
            content=ft.Row([], expand=False, spacing=0),
            bgcolor=theme.colors.primary_lightest,
            border=ft.border.only(
                # left=ft.BorderSide(1, theme.colors.primary_medium),
                # right=ft.BorderSide(1, theme.colors.primary_medium),
                bottom=ft.BorderSide(1, theme.colors.primary_medium),
            ),
            border_radius=ft.border_radius.only(
                top_left=theme.variables.small_radius,
                top_right=theme.variables.small_radius,
            ),
        )
        self.rows = ft.Container(
            content=ft.Column([], expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=0),
            # bgcolor=theme.colors.true_white,
            # border=ft.border.only(
            #     left=ft.BorderSide(1, theme.colors.primary_medium),
            #     right=ft.BorderSide(1, theme.colors.primary_medium),
            #     bottom=ft.BorderSide(1, theme.colors.primary_medium),
            # ),
            expand=True,
            border_radius=ft.border_radius.only(
                bottom_left=theme.variables.small_radius,
                bottom_right=theme.variables.small_radius,
            ),
        )
        self.content = ft.Column([self.header_row, self.rows], spacing=0, expand=True)
        self.row_data = rows
        self.column_data = columns
        self.set_columns(columns)
        self.set_rows(rows)

    def on_header_sorted(self, column_index: int, header: SortableHeader):
        self.sort_ascending = header.sort_mode == SortMode.ASCENDING
        self.sort_column_index = (
            None if header.sort_mode == SortMode.NONE else column_index
        )
        if self.on_sort is not None:
            self.on_sort(column_index)

    def on_row_selected(self, index: int):
        if index in self.selected_row_indices:
            self.selected_row_indices.remove(index)
        else:
            self.selected_row_indices.add(index)

        self.update_selected_rows()
        self.update()

    def on_all_rows_selected(self):
        if self.select_all_checkbox.value:
            for index in range(len(self.row_data)):
                self.selected_row_indices.add(index)
        else:
            self.selected_row_indices.clear()

        self.update_selected_rows()
        self.update()

    def set_columns(self, columns: list[TableColumn]):
        self.column_data = columns
        self.select_all_checkbox = ft.Checkbox(
            on_change=lambda evt: self.on_all_rows_selected(),
        )
        self.header_row.content.controls = [
            ft.Container(
                content=self.select_all_checkbox,
                width=40,
                height=self.row_height,
                bgcolor=theme.colors.primary_lightest,
                padding=theme.variables.table_cell_padding,
            ),
            *(
                (
                    SortableHeader(
                        sort_key=column.key,
                        name=column.label,
                        sort_mode=(
                            SortMode.NONE
                            if column.on_sort is None
                            else SortMode.UNSORTED
                        ),
                        on_sort=lambda header, i=index: self.on_header_sorted(
                            i, header
                        ),
                        expand=column.expand,
                        bgcolor=theme.colors.primary_lightest,
                        width=column.width,
                        height=self.row_height,
                    )
                )
                for index, column in enumerate(columns)
            ),
        ]

    def update_selected_rows(self):
        self.select_all_checkbox.value = len(self.selected_row_indices) >= len(
            self.row_data
        )
        for index, row in enumerate(self.rows.content.controls):
            row.bgcolor = (
                theme.colors.primary_white
                if index in self.selected_row_indices
                else (
                    theme.colors.true_white
                    if index % 2 == 0
                    else theme.colors.off_white
                )
            )
            checkbox = row.content.controls[0].content
            checkbox.value = index in self.selected_row_indices

    def set_rows(self, rows: list[list[TableCell]]):
        self.row_data = rows
        self.rows.content.controls = [
            ft.Container(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Checkbox(
                                value=index in self.selected_row_indices,
                                on_change=lambda evt, i=index: self.on_row_selected(i),
                            ),
                            padding=theme.variables.table_cell_padding,
                            width=40,
                            height=self.row_height,
                        ),
                        *(
                            self._create_row(index, cell)
                            for index, cell in enumerate(row)
                        ),
                    ],
                    spacing=0,
                ),
                expand=True,
            )
            for index, row in enumerate(rows)
        ]
        self.update_selected_rows()

    def _create_row(self, index: int, cell: TableCell) -> ft.Container:
        column = self.column_data[index]
        return ft.Container(
            content=cell.control,
            expand=column.expand,
            height=self.row_height,
            width=column.width,
            padding=None,
        )
