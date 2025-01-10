# pylint: disable=too-many-instance-attributes
"""
The single class that stores all data needed to work on a project
"""
from typing import Callable, Iterable

from adaptation_pathways.app.model.sorting import SortingInfo, SortTarget

from .action import Action
from .metric import Metric, MetricEffect, MetricOperation, MetricValue, MetricValueState
from .pathway import Pathway
from .scenario import Scenario


class PathwaysProject:
    def __init__(
        self,
        project_id: str,
        name: str,
        organization: str,
        start_year: int,
        end_year: int,
        conditions: list[Metric],
        criteria: list[Metric],
        scenarios: list[Scenario],
        actions: list[Action],
        pathways: list[Pathway],
        root_action: Action,
        root_pathway_id: str,
    ):
        self.id = project_id
        self.name = name
        self.organization = organization
        self.start_year = start_year
        self.end_year = end_year
        self._current_id = 0

        self.metrics_by_id: dict[str, Metric] = {}
        for metric in conditions:
            self.metrics_by_id[metric.id] = metric

        for metric in criteria:
            self.metrics_by_id[metric.id] = metric

        self.scenarios_by_id: dict[str, Scenario] = {}
        for scenario in scenarios:
            self.scenarios_by_id[scenario.id] = scenario

        self.actions_by_id: dict[str, Action] = {}
        self.actions_by_id[root_action.id] = root_action
        for action in actions:
            self.actions_by_id[action.id] = action

        self.pathways_by_id: dict[str, Pathway] = {}
        for pathway in pathways:
            self.pathways_by_id[pathway.id] = pathway

        self.condition_sorting = SortingInfo([metric.id for metric in conditions])
        self.criteria_sorting = SortingInfo([metric.id for metric in criteria])
        self.scenario_sorting = SortingInfo([scenario.id for scenario in scenarios])
        self.action_sorting = SortingInfo([action.id for action in actions])
        self.pathway_sorting = SortingInfo([pathway.id for pathway in pathways])

        self.root_pathway_id = root_pathway_id
        self.selected_condition_ids: set[str] = set()
        self.selected_criteria_ids: set[str] = set()
        self.selected_action_ids: set[str] = set()
        self.selected_pathway_ids: set[str] = set()
        self.selected_scenario_id: str = "" if len(scenarios) == 0 else scenarios[0].id
        self.graph_metric_id: str = conditions[0].id

        self.on_conditions_changed: list[Callable[[], None]] = []
        self.on_criteria_changed: list[Callable[[], None]] = []
        self.on_scenarios_changed: list[Callable[[], None]] = []
        self.on_actions_changed: list[Callable[[], None]] = []
        self.on_action_color_changed: list[Callable[[], None]] = []
        self.on_pathways_changed: list[Callable[[], None]] = []

    def __hash__(self):
        return self.id.__hash__()

    def notify_conditions_changed(self):
        for listener in self.on_conditions_changed:
            listener()

    def notify_criteria_changed(self):
        for listener in self.on_criteria_changed:
            listener()

    def notify_scenarios_changed(self):
        for listener in self.on_scenarios_changed:
            listener()

    def notify_actions_changed(self):
        for listener in self.on_actions_changed:
            listener()

    def notify_action_color_changed(self):
        for listener in self.on_action_color_changed:
            listener()

    def notify_pathways_changed(self):
        for listener in self.on_pathways_changed:
            listener()

    @property
    def sorted_actions(self):
        return (
            self.get_action(action_id) for action_id in self.action_sorting.sorted_ids
        )

    @property
    def sorted_conditions(self):
        return (
            self.get_metric(metric_id)
            for metric_id in self.condition_sorting.sorted_ids
        )

    @property
    def sorted_criteria(self):
        return (
            self.get_metric(metric_id) for metric_id in self.criteria_sorting.sorted_ids
        )

    @property
    def sorted_scenarios(self):
        return (
            self.get_scenario(scenario_id)
            for scenario_id in self.scenario_sorting.sorted_ids
        )

    @property
    def sorted_pathways(self):
        return (
            self.get_pathway(pathway_id)
            for pathway_id in self.pathway_sorting.sorted_ids
        )

    @property
    def root_pathway(self):
        return self.get_pathway(self.root_pathway_id)

    @property
    def graph_metric(self):
        return self.get_metric(self.graph_metric_id)

    def _create_id(self) -> str:
        self._current_id += 1
        return str(self._current_id)

    def get_metric(self, metric_id: str) -> Metric | None:
        return self.metrics_by_id.get(metric_id, None)

    def all_metrics(self):
        for metric_id in self.condition_sorting.sorted_ids:
            yield self.get_metric(metric_id)
        for metric_id in self.criteria_sorting.sorted_ids:
            yield self.get_metric(metric_id)

    def _create_metric(self, name: str) -> Metric:
        metric_id = self._create_id()
        metric = Metric(metric_id, name, 0, "")
        self.metrics_by_id[metric.id] = metric
        for action in self.sorted_actions:
            action.metric_data[metric_id] = MetricEffect(0, MetricOperation.ADD)
        return metric

    def create_condition(self) -> Metric:
        metric = self._create_metric("New Condition")
        self.condition_sorting.sorted_ids.append(metric.id)
        return metric

    def create_criteria(self) -> Metric:
        metric = self._create_metric("New Criteria")
        self.criteria_sorting.sorted_ids.append(metric.id)
        return metric

    def delete_condition(self, metric_id: str) -> Metric | None:
        metric = self.metrics_by_id.pop(metric_id)
        self.condition_sorting.sorted_ids.remove(metric_id)
        self.selected_condition_ids.remove(metric_id)
        return metric

    def delete_criteria(self, metric_id: str) -> Metric | None:
        metric = self.metrics_by_id.pop(metric_id)
        self.criteria_sorting.sorted_ids.remove(metric_id)
        self.selected_criteria_ids.remove(metric_id)
        return metric

    def get_scenario(self, scenario_id: str) -> Scenario | None:
        return self.scenarios_by_id.get(scenario_id, None)

    def create_scenario(self) -> Scenario:
        scenario_id = self._create_id()
        scenario = Scenario(scenario_id, "New Scenario", {})
        self.scenarios_by_id[scenario.id] = scenario
        self.scenario_sorting.sorted_ids.append(scenario.id)
        return scenario

    def delete_scenario(self, scenario_id: str) -> Scenario | None:
        scenario = self.scenarios_by_id.pop(scenario_id)
        self.scenario_sorting.sorted_ids.remove(scenario_id)
        return scenario

    def get_action(self, action_id: str) -> Action:
        return self.actions_by_id[action_id]

    def create_action(self, color, icon) -> Action:
        action_id = self._create_id()
        action = Action(
            action_id,
            "New Action",
            color,
            icon,
            {
                metric.id: MetricEffect(0, MetricOperation.ADD)
                for metric in self.all_metrics()
            },
        )

        self.actions_by_id[action.id] = action
        self.action_sorting.sorted_ids.append(action.id)
        return action

    def delete_action(self, action_id: str) -> Action | None:
        action = self.actions_by_id.pop(action_id)
        self.action_sorting.sorted_ids.remove(action_id)
        return action

    def delete_selected_actions(self):
        pathway_ids_to_delete: list[str] = []

        for action_id in self.selected_action_ids:
            self.delete_action(action_id)
            for pathway in self.sorted_pathways:
                if pathway.action_id == action_id:
                    pathway_ids_to_delete.append(pathway.id)

        self.selected_action_ids.clear()
        self.delete_pathways(pathway_ids_to_delete)

    def sort_actions(self):
        if self.action_sorting.target is SortTarget.METRIC:
            sorting_metric = self.get_metric(self.action_sorting.sort_key)

            if sorting_metric is not None:

                def sort_by_metric(action_id: str):
                    action = self.get_action(action_id)
                    if action is None:
                        return 0
                    data = action.metric_data.get(sorting_metric.id, None)
                    return data.value if data is not None else 0

                self.action_sorting.sorted_ids.sort(
                    key=sort_by_metric,
                    reverse=not self.action_sorting.ascending,
                )

        elif self.action_sorting.target is SortTarget.ATTRIBUTE:

            def sort_by_attr(action_id: str):
                if self.action_sorting.sort_key is None:
                    return ""
                action = self.get_action(action_id)
                return getattr(action, self.action_sorting.sort_key, "")

            self.action_sorting.sorted_ids.sort(
                key=sort_by_attr, reverse=not self.action_sorting.ascending
            )

        else:
            self.action_sorting.ascending = True
            self.action_sorting.sort_by_id()

    def get_pathway(self, pathway_id: str) -> Pathway | None:
        if pathway_id is None:
            return None
        return self.pathways_by_id.get(pathway_id, None)

    def create_pathway(
        self, action_id: str, parent_pathway_id: str | None = None
    ) -> Pathway:
        pathway = Pathway(action_id, parent_pathway_id)
        self.pathways_by_id[pathway.id] = pathway
        self.pathway_sorting.sorted_ids.append(pathway.id)
        for metric in self.all_metrics():
            self.update_pathway_values(metric.id)

        return pathway

    def update_pathway_values(self, metric_id: str):
        metric = self.get_metric(metric_id)
        if metric is None:
            return

        updated_pathways: set[str] = set()
        for pathway in self.sorted_pathways:
            self._update_pathway_value(pathway, metric, updated_pathways)

    def _update_pathway_value(
        self, pathway: Pathway, metric: Metric, updated_pathway_ids: set[str]
    ):
        pathway_action = self.get_action(pathway.action_id)
        parent = self.get_pathway(pathway.parent_id)
        current_value = pathway.metric_data.get(metric.id, None)

        # Initialize the value if there was none
        if current_value is None:
            current_value = MetricValue(
                0,
                (
                    MetricValueState.ESTIMATE
                    if parent is not None
                    else MetricValueState.BASE
                ),
            )
            pathway.metric_data[metric.id] = current_value

        # If we have a non-estimate value, we don't need to update anything
        if current_value.state != MetricValueState.ESTIMATE:
            updated_pathway_ids.add(pathway.id)
            return

        if parent.id not in updated_pathway_ids and parent_value.is_estimate:
            self._update_pathway_value(parent, metric, updated_pathway_ids)

        base_value = 0
        if parent is not None:
            parent_value = parent.metric_data.get(metric.id, None)
            if parent_value is not None:
                base_value = parent_value.value

        current_value.value = pathway_action.apply_effect(metric.id, base_value)
        updated_pathway_ids.add(pathway.id)

    def delete_pathway(self, pathway_id: str) -> Pathway | None:
        pathway = self.pathways_by_id.pop(pathway_id, None)
        self.pathway_sorting.sorted_ids.remove(pathway_id)
        return pathway

    def delete_pathways(self, pathway_ids: Iterable[str]):
        ids_to_delete: set[str] = set()
        ids_to_delete.update(pathway_ids)

        # Delete any orphaned children
        for pathway in self.sorted_pathways:
            if pathway.id in ids_to_delete:
                continue

            for ancestor in self.get_ancestors(pathway):
                if ancestor.id in ids_to_delete:
                    ids_to_delete.add(pathway.id)

        for pathway_id in ids_to_delete:
            self.delete_pathway(pathway_id)

    def delete_selected_pathways(self):
        self.delete_pathways(self.selected_pathway_ids)
        self.selected_pathway_ids.clear()

    def sort_pathways(self):
        if self.pathway_sorting.target is SortTarget.METRIC:
            sorting_metric = self.get_metric(self.pathway_sorting.sort_key)

            if sorting_metric is not None:

                def sort_by_metric(pathway_id: str):
                    pathway = self.get_pathway(pathway_id)
                    if pathway is None:
                        return 0

                    data = pathway.metric_data.get(sorting_metric.id, None)
                    return data.value if data is not None else 0

                self.pathway_sorting.sorted_ids.sort(
                    key=sort_by_metric,
                    reverse=not self.pathway_sorting.ascending,
                )

        elif self.pathway_sorting.target is SortTarget.ATTRIBUTE:

            def sort_by_attr(pathway_id: str):
                if self.pathway_sorting.sort_key is None:
                    return ""
                pathway = self.get_pathway(pathway_id)
                return getattr(pathway, self.pathway_sorting.sort_key, "")

            self.pathway_sorting.sorted_ids.sort(
                key=sort_by_attr, reverse=not self.pathway_sorting.ascending
            )

        else:
            self.pathway_sorting.ascending = True
            self.pathway_sorting.sort_by_id()

    def get_children(self, pathway_id: str):
        return (
            pathway
            for pathway in self.sorted_pathways
            if pathway.parent_id == pathway_id
        )

    def get_ancestors(self, pathway: Pathway):
        if pathway.parent_id is None:
            return

        current_pathway = self.get_pathway(pathway.parent_id)
        while current_pathway is not None:
            yield current_pathway
            if current_pathway.parent_id is None:
                return
            current_pathway = self.get_pathway(current_pathway.parent_id)

    def get_ancestors_and_self(self, pathway: Pathway):
        current_pathway: Pathway | None = pathway
        while current_pathway is not None:
            yield current_pathway
            if current_pathway.parent_id is not None:
                current_pathway = self.get_pathway(current_pathway.parent_id)
            else:
                current_pathway = None
