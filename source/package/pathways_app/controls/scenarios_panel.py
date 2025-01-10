import flet as ft
from controls.styled_button import StyledButton
from controls.styled_dropdown import StyledDropdown
from controls.styled_table import StyledTable, TableCell, TableColumn

from adaptation_pathways.app.model.pathways_project import PathwaysProject


class ScenariosPanel(ft.Column):
    def __init__(self, project: PathwaysProject):
        super().__init__(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            scroll=ft.ScrollMode.AUTO,
        )

        self.project = project
        year_range = range(self.project.start_year, self.project.end_year)
        current_scenario = self.project.get_scenario(self.project.selected_scenario_id)
        if current_scenario is None:
            return

        self.controls = [
            ft.Text("!! UNDER CONSTRUCTION !!", color="#FF0000"),
            ft.Row(
                expand=False,
                controls=[
                    StyledDropdown(
                        value=current_scenario.name,
                        options=[
                            ft.dropdown.Option(key=scenario.id, text=scenario.name)
                            for scenario in self.project.sorted_scenarios
                        ],
                    ),
                    ft.Container(expand=True),
                    StyledButton("New", icon=ft.icons.ADD_CIRCLE_OUTLINE),
                ],
            ),
            StyledTable(
                columns=[
                    TableColumn(label="Year"),
                    *(
                        TableColumn(label=metric.name)
                        for metric in self.project.sorted_conditions
                    ),
                ],
                rows=[
                    [
                        TableCell(ft.Text(year)),
                        *(
                            TableCell(
                                ft.Text(data or "None")
                            )
                            for data in [
                                current_scenario.get_data(year, metric)
                                for metric in self.project.sorted_conditions
                            ]
                        ),
                    ]
                    for year in year_range
                ],
            ),
        ]

    def redraw(self):
        pass
