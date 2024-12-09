from typing import Optional

import numpy as np

from ..action_instance import ActionInstance
from ..app.model.action import Action
from ..app.model.metric import Metric
from ..app.model.scenario import Scenario
from ..sequence import Sequence
from ._evaluate_criterion import evaluate_criterion


class PathwaysInputGenerator:
    def __init__(
        self,
        sequences: list[Sequence],
        scenario: Scenario,
        tippingpoint_metric: Metric,
        action_instances: list[ActionInstance],
    ):
        """
        Initializes the PathwaysInputGenerator.

        :param sequences: list of Sequence objects.
        :param scenario: Optional dictionary with time-series information.
        :param tippingpoint_metric: Metric used to determine timing/position of actions in pathways
        """
        self.filtered_sequences = [
            sequence for sequence in sequences if not sequence.filters.filtered_out
        ]

        self.scenario = scenario
        self.action_instances = (
            action_instances if action_instances is not None else []
        )  # Will hold ActionInstance objects
        self.tippingpoint_metric = tippingpoint_metric
        self.instance_count: dict[Action, list] = {}

    @staticmethod
    def aggregate_effectiveness(sequence: Sequence, up_to_index: int) -> dict:
        """
        Aggregates effectiveness values for the actions in a sequence up to the given index.

        :param sequence: The Sequence object.
        :param up_to_index: The index up to which effectiveness is aggregated.
        :return: Dictionary of Metric, MetricValue for instance.
        """
        evaluation_results = {}
        for key in sequence.actions[0].metric_data.keys():
            metrics = [
                action.metric_data[key]
                for action in sequence.actions
                if key in action.metric_data and action.metric_data[key] is not None
            ]
            evaluation_results[key] = evaluate_criterion(metrics, up_to_index)
        return evaluation_results

    def interpolate_time(
        self, tipping_point_value: float, metric: Metric
    ) -> Optional[float]:
        """
        Interpolates the time for a given tipping point value based on the scenario time-series.

        :param tipping_point_value: Value of the metric to determine the tipping point.
        :param metric: The Metric object for which the time is to be interpolated.
        :return: Interpolated time for the tipping point value.
        """
        if not self.scenario:
            raise ValueError("No scenario provided to interpolate time.")

        # Retrieve the time-series data for the specified metric
        time_series = self.scenario.metric_data_over_time.get(metric, [])
        if time_series == []:
            raise ValueError(f"No time-series data found for metric: {metric.name}")

        # Extract times and data values
        times = np.array(
            [point.time for point in time_series if point.time is not None]
        )
        data_values = np.array([point.data.value for point in time_series])

        if tipping_point_value in data_values:
            idx = np.where(data_values == tipping_point_value)[0][0]
            return float(int(times[idx]))
        idx = np.searchsorted(data_values, tipping_point_value)
        if idx == 0 or idx == len(data_values):
            raise ValueError(
                f"The time-series is too short for the given tipping point value "
                f"({tipping_point_value}). "
                f"It only captures the range from {data_values[0]} at time {times[0]} "
                f"to {data_values[-1]} at time {times[-1]}."
            )

        # Get the points around the value for interpolation
        lower_value, upper_value = data_values[idx - 1], data_values[idx]
        lower_time, upper_time = times[idx - 1], times[idx]

        # Perform linear interpolation
        interpolated_time = lower_time + (upper_time - lower_time) * (
            (tipping_point_value - lower_value) / (upper_value - lower_value)
        )
        return float(int(interpolated_time))

    def generate_action_instances(
        self,
        end_current_system: float,
    ):
        """
        Creates ActionInstance objects for each action in the sequences.

        :param end_current_system: Tipping point of the current system.
        """

        for sequence in self.filtered_sequences:
            for idx, action in enumerate(sequence.actions):
                precondition = sequence.actions[
                    :idx
                ]  # All elements up to (excluding) the current element
                if action not in self.instance_count:
                    self.instance_count[action] = []
                if precondition not in self.instance_count[action]:
                    self.instance_count[action].append(precondition)
                unique_instance = self.instance_count[action].index(precondition)

                # Aggregate effectiveness
                instance_performance = self.aggregate_effectiveness(sequence, idx)

                tipping_point_value = instance_performance[
                    self.tippingpoint_metric
                ].value

                # Determine tipping point (xposition)
                time_series = self.scenario.metric_data_over_time.get(
                    self.tippingpoint_metric, []
                )
                if time_series == []:
                    tipping_point_xposition = tipping_point_value + end_current_system
                else:
                    tipping_point_xposition = self.interpolate_time(
                        tipping_point_value + end_current_system,
                        self.tippingpoint_metric,
                    )

                # Create ActionInstance
                action_instance = ActionInstance(
                    action=action,
                    instance=unique_instance,
                    tipping_point=tipping_point_xposition,
                    metric_data=instance_performance,
                )
                print(
                    action.name,
                    unique_instance,
                    tipping_point_value,
                    tipping_point_xposition,
                )
                self.action_instances.append(action_instance)

    def create_xpositions_file(self, output_file: str, end_current_system: float):
        """
        Creates the xpositions.txt file from the ActionInstance objects.

        :param end_current_system: Tipping point of the current system.
        :param output_file: The name of the output file.
        """
        time_series = self.scenario.metric_data_over_time.get(
            self.tippingpoint_metric, False
        )
        if time_series != []:
            xpositions_list = [
                (
                    "current",
                    self.interpolate_time(end_current_system, self.tippingpoint_metric),
                )
            ]
        else:
            xpositions_list = [("current", end_current_system)]

        for instance in self.action_instances:
            xposition_value = instance.tipping_point
            action_key = f"{instance.action.name.replace(' ', '')}[{instance.instance}]"
            xpositions_list.append((action_key, xposition_value))
        xpositions_list = list(set(xpositions_list))
        # Write the file
        with open(output_file, "w", encoding="utf-8") as file:
            for key, value in xpositions_list:
                file.write(f"{key} {value}\n")

        print(f"File '{output_file}' created successfully.")

    def create_sequences_file(self, output_file: str):
        """
        Creates the sequences.txt file from the ActionInstance objects.

        :param output_file: The name of the output file.
        """
        sequences_list = []

        # Process single-action sequences
        sequences_list.extend(self._process_single_action_sequences())

        # Process multi-action sequences
        sequences_list.extend(self._process_multi_action_sequences())

        # Remove duplicates from the list
        sequences_list = list(set(sequences_list))

        # Write the file
        with open(output_file, "w", encoding="utf-8") as file:
            for col1, col2 in sequences_list:
                file.write(f"{col1} {col2}\n")

        print(f"File '{output_file}' created successfully.")

    def _process_single_action_sequences(self) -> list[tuple[str, str]]:
        """
        Processes sequences with only one action.

        :return: A list of tuples representing single-action sequences.
        """
        sequences_list = []

        for sequence in self.filtered_sequences:
            if len(sequence.actions) == 1:
                first_action = sequence.actions[0]
                first_precondition = sequence.actions[:0]
                first_idx = self.instance_count[first_action].index(first_precondition)
                first_key = f"{first_action.name.replace(' ', '')}[{first_idx}]"

                if ("current", first_key) not in sequences_list:
                    sequences_list.append(("current", first_key))

        return sequences_list

    def _process_multi_action_sequences(self) -> list[tuple[str, str]]:
        """
        Processes sequences with multiple actions.

        :return: A list of tuples representing multi-action sequences.
        """
        sequences_list = []

        for sequence in self.filtered_sequences:
            for i in range(len(sequence.actions) - 1):
                first_action = sequence.actions[i]
                second_action = sequence.actions[i + 1]

                # Identify preconditions and their indices for both actions
                first_precondition = sequence.actions[:i]
                second_precondition = sequence.actions[: i + 1]

                first_idx = self.instance_count[first_action].index(first_precondition)
                second_idx = self.instance_count[second_action].index(
                    second_precondition
                )

                first_key = f"{first_action.name.replace(' ', '')}[{first_idx}]"
                second_key = f"{second_action.name.replace(' ', '')}[{second_idx}]"

                if ("current", first_key) not in sequences_list:
                    sequences_list.append(("current", first_key))
                if (first_key, second_key) not in sequences_list:
                    sequences_list.append((first_key, second_key))

        return sequences_list

    def generate_input_files(
        self,
        sequence_file: str = "sequences.txt",
        xposition_file: str = "xpositions.txt",
        end_current_system: float = 0,
    ):
        """
        Generates all input files for the Pathways Generator.

        :param sequence_file: File to store sequences.
        :param xposition_file: File to store xpositions.
        :param end_current_system: Tipping point of the current system.
        """
        self.generate_action_instances(end_current_system)
        self.create_xpositions_file(xposition_file, end_current_system)
        self.create_sequences_file(sequence_file)
