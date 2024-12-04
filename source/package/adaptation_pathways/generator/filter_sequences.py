import random

from ..app.model.comparisons import NumberComparison
from ..app.model.filter import MetricFilter
from ..sequence import Sequence


class SequenceFilter:
    def __init__(
        self,
        sequences: list[Sequence],
        filtering_conditions: list[MetricFilter],
        n: int,
    ):
        """
        Initializes the SequenceFilter.

        :param sequences: List of Sequence objects to evaluate and filter.
        :param filtering_conditions: Dict specifying filtering conditions for evaluation criteria.
        :param n: Number of sequences to have finally.
        """
        self.sequences = [
            sequence for sequence in sequences if sequence.is_valid
        ]  # List of Sequence objects
        self.filtering_conditions = filtering_conditions
        self.n = n

    @staticmethod
    def compare_criteria(value, threshold, relation):
        """
        Compares a single evaluation criterion value against a condition.

        :param value: The value to compare (could be string or float).
        :param threshold: Threshold relevant for filtering.
        :param relation: type of filtering.
        :return: True if the value satisfies the condition, False otherwise.
        """

        if not isinstance(value, (int, float)):
            raise ValueError("Value type not supported for filtering.")

        # Apply filtering logic using NumberComparison
        if relation == NumberComparison.GREATER_THAN:
            return value > threshold
        if relation == NumberComparison.LESS_THAN:
            return value < threshold
        if relation == NumberComparison.GREATER_THAN_OR_EQUAL:
            return value >= threshold
        if relation == NumberComparison.LESS_THAN_OR_EQUAL:
            return value <= threshold
        if relation == NumberComparison.EQUAL:
            return value == threshold
        if relation == NumberComparison.DOESNT_EQUAL:
            return value != threshold
        raise ValueError(f"Unknown filter direction: {relation}")

    def filter_sequences(self):
        """
        Filters sequences based on the filtering conditions and updates their filtered_out and
        exclusion_reason attributes.

        :return: None. Updates Sequence objects in place.
        """
        for sequence in self.sequences:
            meets_all_conditions = True
            exclusion_reason = None

            # Check filtering conditions
            for filtering_condition in self.filtering_conditions:
                value = sequence.performance[filtering_condition.metric].value
                threshold = filtering_condition.value
                relation = filtering_condition.relation
                if not self.compare_criteria(value, threshold, relation):
                    meets_all_conditions = False
                    exclusion_reason = "Does not meet conditions"
                    break

            # Update sequence attributes based on filtering conditions
            sequence.filtered_out = not meets_all_conditions
            sequence.exclusion_reason = (
                exclusion_reason if not meets_all_conditions else None
            )

        # Filter out sequences that don't meet conditions
        filtered_sequences = [seq for seq in self.sequences if not seq.filtered_out]

        # Handle shortlist limit
        if len(filtered_sequences) > self.n:
            print(
                f"Number of sequences was {len(filtered_sequences)}, "
                f"but analysis is limited to {self.n} sequences. "
                f"A short-list of {self.n} sequences has been randomly sampled."
            )

            # Randomly sample sequences to meet the limit
            shortlisted = random.sample(filtered_sequences, self.n)

            # Mark sequences filtered out due to exceeding shortlist limit
            for seq in filtered_sequences:
                if seq not in shortlisted:
                    seq.filtered_out = True
                    seq.exclusion_reason = "Exceeded shortlist limit"
