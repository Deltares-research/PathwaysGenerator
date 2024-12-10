from ..app.model.metric import Metric, MetricValue
from ..sequence import Sequence
from ._evaluate_criterion import evaluate_criterion
from ._get_metric_value_by_name import get_metric_value_by_name


class SequenceEvaluator:
    def __init__(
        self,
        sequences: list[Sequence],
        tippingpoint_metric: Metric,
        planning_end: float,
    ):
        """
        Initializes the SequenceEvaluator.
        :param sequences: List of Sequence objects to evaluate.
        :param tippingpoint_metric: Metric object used to determine length of sequence.
        :param planning_end: The target value for planning.
        """
        self.sequences = [
            sequence for sequence in sequences if sequence.filters.is_valid
        ]
        self.tippingpoint_metric = tippingpoint_metric
        self.planning_end = planning_end

    @staticmethod
    def evaluate_criterion(metrics: list[MetricValue], num_needed: int):
        """
        Evaluates a single metric across multiple actions in a sequence.
        :param metrics: List of MetricValue objects from the sequence.
        :param num_needed: int to specify number of actions in Sequence considered for evaluation
        :return: A MetricValue object representing the combined evaluation.
        """
        return evaluate_criterion(metrics, num_needed)

    @staticmethod
    def get_metric_value_by_name(action, metric_name):
        """
        Retrieves a MetricValue object from metric_data of an Action by name of the Metric object.
        :param action: The Action object to query.
        :param metric_name: The name of the Metric to search for.
        :return: The corresponding MetricValue, or None if not found.
        """
        return get_metric_value_by_name(action.metric_data, metric_name)

    def determine_number_needed_actions(self, sequence: Sequence):
        """
        Determines the number of actions needed in a sequence to meet the planning_end.
        :param sequence: The Sequence object to evaluate.
        :return: Number of actions needed to meet the planning_end.
        """
        cumulative_value = 0.0
        for idx, action in enumerate(sequence.actions):
            metric_value = action.metric_data[self.tippingpoint_metric]
            if not metric_value:
                continue

            cumulative_value += metric_value.value
            if cumulative_value >= self.planning_end:
                return idx + 1  # Actions needed is 1-based
        return len(
            sequence.actions
        )  # Default to the full sequence if the target is not met

    def evaluate_sequence(self, sequence: Sequence):
        """
        Evaluates a single sequence across all specified evaluation keys.
        :param sequence: A Sequence object to evaluate.
        :return: Updates the Sequence object with evaluation metrics.
        """
        evaluation_results = {}
        num_needed = self.determine_number_needed_actions(sequence)
        for key in sequence.actions[0].metric_data.keys():
            metrics = [
                action.metric_data[key]
                for action in sequence.actions
                if key in action.metric_data and action.metric_data[key] is not None
            ]
            evaluation_results[key] = evaluate_criterion(metrics, num_needed)

        sequence.performance = evaluation_results
        sequence.actions = sequence.actions[:num_needed]

    def evaluate_all_sequences(self):
        """
        Evaluates all sequences and updates them with performance metrics.
        :return: None. Updates Sequence objects in place.
        """
        unique_sequences = []
        for sequence in self.sequences:
            self.evaluate_sequence(sequence)
            if sequence in unique_sequences:
                sequence.filters.is_valid = False
                sequence.filters.reasoning = (
                    "Part of Sequence used. Identical to other Sequence."
                )
            else:
                unique_sequences.append(sequence)

        print(
            f"Step 2: The performance of each valid sequence ({len(unique_sequences)}) "
            f"was calculated."
        )
