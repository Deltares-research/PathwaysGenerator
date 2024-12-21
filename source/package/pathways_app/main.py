import locale
import logging

import example
import flet as ft
import theme
from controls.actions_panel import ActionsPanel
from controls.graph_panel import GraphPanel
from controls.header import SectionHeader
from controls.menu_bar import MenuBar
from controls.metrics_panel import MetricsPanel
from controls.panel import Panel
from controls.pathways_panel import PathwaysPanel
from controls.scenarios_panel import ScenariosPanel
from controls.tabbed_panel import TabbedPanel


locale.setlocale(locale.LC_ALL, "")


def main(page: ft.Page):
    page.theme = theme.theme
    page.theme_mode = ft.ThemeMode.LIGHT

    # bitdojo_window could make a custom title bar
    # page.window.frameless = True

    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = True

    page.title = "Pathways Generator"
    page.fonts = theme.fonts
    page.bgcolor = theme.colors.primary_darker
    page.padding = 1
    page.spacing = 0

    project = example.project

    page.appbar = MenuBar(project)
    metrics_panel = MetricsPanel(project)
    metrics_tab = (SectionHeader(ft.icons.TUNE, "Metrics"), metrics_panel)

    actions_panel = ActionsPanel(project)
    actions_tab = (
        SectionHeader(ft.icons.CONSTRUCTION_OUTLINED, "Actions"),
        actions_panel,
    )

    scenarios_panel = ScenariosPanel(project)
    scenarios_tab = (
        SectionHeader(ft.icons.PUBLIC, "Scenarios"),
        scenarios_panel,
    )

    graph_panel = GraphPanel(project)
    pathways_panel = PathwaysPanel(project)

    def on_metrics_changed():
        metrics_panel.redraw()
        scenarios_panel.redraw()
        actions_panel.redraw()
        pathways_panel.redraw()
        graph_panel.redraw()

    def on_scenarios_changed():
        scenarios_panel.redraw()
        graph_panel.redraw()

    def on_actions_changed():
        actions_panel.redraw()
        pathways_panel.redraw()
        graph_panel.redraw()

    def on_pathways_changed():
        pathways_panel.redraw()
        graph_panel.redraw()

    def on_action_color_changed():
        pathways_panel.redraw()
        graph_panel.redraw()

    # def on_graph_changed():
    #     graph_panel.redraw()

    project.on_conditions_changed.append(on_metrics_changed)
    project.on_criteria_changed.append(on_metrics_changed)
    project.on_scenarios_changed.append(on_scenarios_changed)
    project.on_actions_changed.append(on_actions_changed)
    project.on_action_color_changed.append(on_action_color_changed)
    project.on_pathways_changed.append(on_pathways_changed)

    page.add(
        ft.Container(
            expand=True,
            padding=theme.variables.panel_spacing,
            content=ft.Row(
                expand=True,
                spacing=theme.variables.panel_spacing,
                controls=[
                    ft.Column(
                        expand=2,
                        spacing=theme.variables.panel_spacing,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            TabbedPanel(
                                selected_index=0,
                                tabs=[metrics_tab, actions_tab, scenarios_tab],
                            )
                        ],
                    ),
                    ft.Column(
                        expand=3,
                        spacing=theme.variables.panel_spacing,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            Panel(graph_panel),
                            Panel(
                                content=ft.Column(
                                    expand=False,
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=15,
                                    controls=[
                                        pathways_panel,
                                    ],
                                ),
                                padding=theme.variables.panel_padding,
                            ),
                        ],
                    ),
                ],
            ),
            bgcolor=theme.colors.primary_lighter,
            border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
        )
    )


logging.basicConfig(level=logging.CRITICAL)
ft.app(target=main, assets_dir="assets")

print("Pathways App Started")
