from ..app.model.comparisons import SequenceComparison


# External validation functions


def validate_starts_with(actions, dependency):
    return actions[0] == dependency.action


def validate_doesnt_start_with(actions, dependency):
    return actions[0] != dependency.action


def validate_contains(actions, dependency):
    return dependency.action in actions


def validate_doesnt_contain(actions, dependency):
    return dependency.action not in actions


def validate_ends_with(actions, dependency):
    return actions[-1] == dependency.action


def validate_doesnt_end_with(actions, dependency):
    return actions[-1] != dependency.action


def validate_blocks(actions, dependency):
    if dependency.action in actions:
        action_index = actions.index(dependency.action)
        for other_action in dependency.other_actions:
            if other_action in actions:
                other_action_index = actions.index(other_action)
                if action_index < other_action_index:
                    return False
    return True


def validate_after(actions, dependency):
    if dependency.action in actions:
        action_index = actions.index(dependency.action)
        for other_action in dependency.other_actions:
            if other_action in actions:
                other_action_index = actions.index(other_action)
                if action_index < other_action_index:
                    return False
    return True


def validate_directly_after(actions, dependency):
    if dependency.action in actions:
        action_index = actions.index(dependency.action)
        for other_action in dependency.other_actions:
            if other_action in actions:
                other_action_index = actions.index(other_action)
                if action_index != other_action_index + 1:
                    return False
    return True


def validate_before(actions, dependency):
    if dependency.action in actions:
        action_index = actions.index(dependency.action)
        for other_action in dependency.other_actions:
            if other_action in actions:
                other_action_index = actions.index(other_action)
                if action_index > other_action_index:
                    return False
    return True


def validate_directly_before(actions, dependency):
    if dependency.action in actions:
        action_index = actions.index(dependency.action)
        for other_action in dependency.other_actions:
            if other_action in actions:
                other_action_index = actions.index(other_action)
                if action_index != other_action_index - 1:
                    return False
    return True


VALIDATION_FUNCTIONS = {
    SequenceComparison.STARTS_WITH: validate_starts_with,
    SequenceComparison.DOESNT_START_WITH: validate_doesnt_start_with,
    SequenceComparison.CONTAINS: validate_contains,
    SequenceComparison.DOESNT_CONTAIN: validate_doesnt_contain,
    SequenceComparison.ENDS_WITH: validate_ends_with,
    SequenceComparison.DOESNT_END_WITH: validate_doesnt_end_with,
    SequenceComparison.BLOCKS: validate_blocks,
    SequenceComparison.AFTER: validate_after,
    SequenceComparison.DIRECTLY_AFTER: validate_directly_after,
    SequenceComparison.BEFORE: validate_before,
    SequenceComparison.DIRECTLY_BEFORE: validate_directly_before,
}
