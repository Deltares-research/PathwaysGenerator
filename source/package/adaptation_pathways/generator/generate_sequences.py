from itertools import permutations

from ..app.model.action import Action, ActionDependency
from ..app.model.comparisons import SequenceComparison
from ..sequence import Sequence


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
                    Sequence(actions=list(combination), performance={})
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

        # Helper to get indices safely
        def get_index(action):
            return actions.index(action) if action in actions else None

        # Common logic for relationships involving multiple actions
        def validate_multiple(action_index, other_actions, condition):
            for other_action in other_actions:
                other_action_index = get_index(other_action)
                if other_action_index is not None and not condition(
                    action_index, other_action_index
                ):
                    return False
            return True

        # Dictionary mapping relations to validation logic
        relation_validators = {
            SequenceComparison.STARTS_WITH: lambda: actions[0] == dependency.action,
            SequenceComparison.DOESNT_START_WITH: lambda: actions[0]
            != dependency.action,
            SequenceComparison.CONTAINS: lambda: dependency.action in actions,
            SequenceComparison.DOESNT_CONTAIN: lambda: dependency.action not in actions,
            SequenceComparison.ENDS_WITH: lambda: actions[-1] == dependency.action,
            SequenceComparison.DOESNT_END_WITH: lambda: actions[-1]
            != dependency.action,
            SequenceComparison.BLOCKS: lambda: (
                validate_multiple(
                    get_index(dependency.action),
                    dependency.other_actions,
                    lambda a_idx, o_idx: a_idx > o_idx,
                )
                if dependency.action in actions
                else True
            ),
            SequenceComparison.AFTER: lambda: (
                validate_multiple(
                    get_index(dependency.action),
                    dependency.other_actions,
                    lambda a_idx, o_idx: a_idx > o_idx,
                )
                if dependency.action in actions
                else True
            ),
            SequenceComparison.DIRECTLY_AFTER: lambda: (
                validate_multiple(
                    get_index(dependency.action),
                    dependency.other_actions,
                    lambda a_idx, o_idx: a_idx == o_idx + 1,
                )
                if dependency.action in actions
                else True
            ),
            SequenceComparison.BEFORE: lambda: (
                validate_multiple(
                    get_index(dependency.action),
                    dependency.other_actions,
                    lambda a_idx, o_idx: a_idx < o_idx,
                )
                if dependency.action in actions
                else True
            ),
            SequenceComparison.DIRECTLY_BEFORE: lambda: (
                validate_multiple(
                    get_index(dependency.action),
                    dependency.other_actions,
                    lambda a_idx, o_idx: a_idx == o_idx - 1,
                )
                if dependency.action in actions
                else True
            ),
        }

        # Validate the dependency using the appropriate logic
        validate = relation_validators.get(dependency.relation)
        return validate() if validate else True

    def filter_sequences(self, sequences: list[Sequence]) -> list[Sequence]:
        """
        Filters out invalid sequences based on dependencies.

        :param sequences: List of Sequence objects.
        :return: list of valid Sequence objects.
        """
        for sequence in sequences:
            sequence.is_valid = self.is_valid_sequence(sequence)
        return [seq for seq in sequences if seq.is_valid]

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
