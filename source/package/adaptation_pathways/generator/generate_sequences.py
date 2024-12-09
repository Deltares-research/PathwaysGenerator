from itertools import permutations

from ..app.model.action import Action, ActionDependency
from ..sequence import Sequence, SequenceFilter
from ._validate_action_requirements import VALIDATION_FUNCTIONS


class SequenceGenerator:
    def __init__(
        self,
        actions: list[Action],
        dependencies: list[ActionDependency],
        max_length: int,
    ):
        """
        Initializes the SequenceGenerator.

        :param actions: List of Action objects.
        :param dependencies: List of ActionDependency objects that define rules.
        :param max_length: Maximum number of elements in a sequence.
        """
        self.actions = actions
        self.dependencies = dependencies
        self.max_length = max_length

    def generate_combinations(self) -> list[Sequence]:
        """
        Generates all possible permutations of actions up to the max length.

        :return: List of Sequence objects.
        """
        possible_sequences = []
        for length in range(1, self.max_length + 1):
            for combination in permutations(self.actions, length):
                possible_sequences.append(
                    Sequence(
                        actions=list(combination),
                        performance={},
                        filters=SequenceFilter(
                            is_valid=True, filtered_out=True, reasoning=""
                        ),
                    )
                )
        return possible_sequences

    def is_valid_sequence(self, sequence: Sequence) -> bool:
        """
        Validates a Sequence object based on dependencies.

        :param sequence: A Sequence object.
        :return: True if the sequence is valid, False otherwise.
        """
        for dependency in self.dependencies:
            if not self._validate_dependency(sequence.actions, dependency):
                return False
        return True

    @staticmethod
    def _validate_dependency(
        actions: list[Action], dependency: ActionDependency
    ) -> bool:
        """
        Validates a single dependency for a sequence of actions.

        :param actions: List of Action objects in a sequence.
        :param dependency: An ActionDependency object.
        :return: True if the sequence satisfies the dependency, False otherwise.
        """
        validate_func = VALIDATION_FUNCTIONS.get(dependency.relation)
        if not validate_func:
            return True  # Default to True if no matching validation logic exists
        return validate_func(actions, dependency)

    def filter_sequences(self, sequences: list[Sequence]) -> list[Sequence]:
        """
        Filters out invalid sequences based on dependencies.

        :param sequences: List of Sequence objects.
        :return: list of valid Sequence objects.
        """
        for sequence in sequences:
            sequence.filters.is_valid = self.is_valid_sequence(sequence)
        return [seq for seq in sequences if seq.filters.is_valid]

    def generate_filtered_sequences(self) -> list[Sequence]:
        """
        Generates and filters sequences.

        :return: List of valid Sequence objects.
        """
        # Generate all possible combinations
        possible_sequences = self.generate_combinations()

        # Filter the sequences
        valid_sequences = self.filter_sequences(possible_sequences)
        print(f"Step 1: {len(valid_sequences)} valid sequences were generated.")
        return valid_sequences
