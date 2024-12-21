# pylint: disable=too-many-arguments
import flet as ft
import theme


class StyledTable(ft.DataTable):
    def __init__(
        self,
        columns: list[ft.DataColumn],
        rows: list[ft.DataRow],
        row_height=36,
        sort_column_index: int | None = None,
        sort_ascending: bool | None = None,
        show_checkboxes=False,
    ):
        super().__init__(
            expand=True,
            horizontal_margin=0,
            show_checkbox_column=show_checkboxes,
            checkbox_horizontal_margin=theme.variables.table_cell_padding.left,
            columns=columns,
            rows=rows,
            bgcolor=theme.colors.true_white,
            sort_column_index=sort_column_index,
            sort_ascending=sort_ascending,
            column_spacing=20,
            data_row_min_height=0,
            data_row_max_height=row_height,
            data_row_color={
                ft.ControlState.HOVERED: theme.colors.off_white,
                ft.ControlState.FOCUSED: theme.colors.off_white,
                ft.ControlState.SELECTED: theme.colors.primary_white,
                ft.ControlState.PRESSED: theme.colors.off_white,
                ft.ControlState.DRAGGED: theme.colors.off_white,
                ft.ControlState.SCROLLED_UNDER: theme.colors.off_white,
            },
            divider_thickness=0,
            horizontal_lines=ft.BorderSide(1, theme.colors.primary_lightest),
            heading_row_height=30,
            heading_row_color=theme.colors.primary_lightest,
            heading_text_style=theme.text.table_header,
            border=ft.border.all(1, theme.colors.primary_light),
        )

        self.set_columns(columns)
        self.set_rows(rows)

    def set_columns(self, columns: list[ft.DataColumn]):
        for column in columns:
            column.label = ft.Container(
                content=column.label,
                expand=True,
                padding=theme.variables.table_cell_padding,
            )
        self.columns = columns

    def set_rows(self, rows: list[ft.DataRow]):
        for row in rows:
            for cell in row.cells:
                cell.content = ft.Container(
                    content=cell.content,
                    padding=theme.variables.table_cell_padding,
                )

        self.rows = rows
