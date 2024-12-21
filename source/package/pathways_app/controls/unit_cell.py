from typing import Callable

import flet as ft
import theme

from adaptation_pathways.app.model.metric import Metric, MetricUnit, default_units


class MetricUnitCell(ft.DataCell):
    def __init__(
        self,
        metric: Metric,
        on_unit_change: Callable[["MetricUnitCell"], None] | None = None,
    ):
        self.metric = metric

        def on_default_metric_selected(unit: str):
            self.metric.unit_or_default = unit
            if on_unit_change is not None:
                on_unit_change(self)

        def create_unit_button(unit: MetricUnit):
            return ft.MenuItemButton(
                key=unit.symbol,
                content=ft.Text(unit.name, style=theme.text.normal),
                style=theme.buttons.submenu,
                on_click=lambda e, u=unit: on_default_metric_selected(u.symbol),
            )

        def create_unit_submenu(name: str, controls: ft.Control):
            return ft.SubmenuButton(
                ft.Text(name, style=theme.text.normal),
                style=theme.buttons.submenu,
                controls=controls,
            )

        def create_submenu_header(text: str):
            return ft.Container(
                ft.Text(value=text.upper(), style=theme.text.submenu_header),
                padding=ft.padding.only(left=4, right=4, top=8, bottom=4),
                bgcolor=theme.colors.true_white,
                expand=True,
            )

        super().__init__(
            ft.MenuBar(
                style=theme.buttons.menu_button,
                controls=[
                    ft.SubmenuButton(
                        expand=False,
                        style=theme.buttons.submenu,
                        content=ft.Text(
                            metric.unit.display_name, style=theme.text.normal
                        ),
                        controls=[
                            create_unit_submenu(
                                "Length",
                                [
                                    create_submenu_header("SI"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.length.si
                                    ),
                                    create_submenu_header("Imperial"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.length.imperial
                                    ),
                                ],
                            ),
                            create_unit_submenu(
                                "Area",
                                [
                                    create_submenu_header("SI"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.area.si
                                    ),
                                    create_submenu_header("Imperial"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.area.imperial
                                    ),
                                ],
                            ),
                            create_unit_submenu(
                                "Volume",
                                [
                                    create_submenu_header("SI"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.volume.si
                                    ),
                                    create_submenu_header("Imperial"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.volume.imperial
                                    ),
                                ],
                            ),
                            create_unit_submenu(
                                "Temperature",
                                [
                                    create_submenu_header("SI"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.temperature.si
                                    ),
                                    create_submenu_header("Imperial"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.temperature.imperial
                                    ),
                                ],
                            ),
                            create_unit_submenu(
                                "Velocity",
                                [
                                    create_submenu_header("SI"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.velocity.si
                                    ),
                                    create_submenu_header("Imperial"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.velocity.imperial
                                    ),
                                ],
                            ),
                            create_unit_submenu(
                                "Acceleration",
                                [
                                    create_submenu_header("SI"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.acceleration.si
                                    ),
                                    create_submenu_header("Imperial"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.acceleration.imperial
                                    ),
                                ],
                            ),
                            create_unit_submenu(
                                "Mass/Weight",
                                [
                                    create_submenu_header("SI"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.mass_weight.si
                                    ),
                                    create_submenu_header("Imperial"),
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.mass_weight.imperial
                                    ),
                                ],
                            ),
                            create_unit_submenu(
                                "Time",
                                [
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.time
                                    ),
                                ],
                            ),
                            create_unit_submenu(
                                "Currency",
                                [
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.currency
                                    ),
                                ],
                            ),
                            create_unit_submenu(
                                "Relative",
                                [
                                    *(
                                        create_unit_button(unit)
                                        for unit in default_units.relative
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            )
        )
