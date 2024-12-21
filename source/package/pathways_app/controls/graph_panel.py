import flet as ft
import matplotlib.pyplot
import theme
from controls.styled_button import StyledButton
from controls.styled_dropdown import StyledDropdown
from flet.matplotlib_chart import MatplotlibChart

from adaptation_pathways.app.model.pathways_project import PathwaysProject
from adaptation_pathways.app.service.plotting_service import PlottingService


class GraphPanel(ft.Row):
    def __init__(self, project: PathwaysProject):
        super().__init__(expand=False, spacing=0)

        self.project = project

        self.graph_container = ft.Container(
            expand=True, bgcolor=theme.colors.true_white
        )

        self.metric_dropdown = StyledDropdown(
            value="",
            options=[],
            width=200,
        )

        self.update_parameters()

        self.controls = [
            ft.Container(
                expand=False,
                padding=theme.variables.panel_padding,
                content=ft.Column(
                    expand=False,
                    width=200,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        StyledDropdown(
                            "Metro Map",
                            options=[
                                ft.dropdown.Option("Metro Map"),
                                ft.dropdown.Option("Bar Chart"),
                            ],
                            option_icons=[ft.icons.ROUTE_OUTLINED, ft.icons.BAR_CHART],
                            height=36,
                            text_style=theme.text.dropdown_large,
                        ),
                        ft.Container(expand=True),
                        ft.Row(
                            [
                                StyledButton("Export", icon=ft.icons.SAVE_SHARP),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                ),
            ),
            ft.Container(
                expand=True,
                bgcolor=theme.colors.true_white,
                border_radius=ft.border_radius.only(
                    top_right=theme.variables.small_radius,
                    bottom_right=theme.variables.small_radius,
                ),
                padding=ft.padding.only(bottom=10),
                content=ft.Column(
                    [self.graph_container, self.metric_dropdown],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        ]

        self.update_graph()

    def redraw(self):
        self.update_parameters()
        self.update_graph()
        self.update()

    def update_parameters(self):
        self.metric_dropdown.options = [
            *(
                ft.dropdown.Option(
                    key=metric.id, text=f"{metric.name} ({metric.unit.symbol})"
                )
                for metric in self.project.sorted_conditions
            ),
        ]
        self.metric_dropdown.value = self.project.graph_metric_id

    def update_graph(self):
        figure, _ = PlottingService.draw_metro_map(self.project)
        self.graph_container.content = MatplotlibChart(figure)
        matplotlib.pyplot.close(figure)
