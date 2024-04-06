import copy
import sqlite3
from pathlib import Path

from .. import alias
from ..action import Action
from ..action_combination import ActionCombination
from ..plot.colour import default_node_colour, hex_to_rgba, rgba_to_hex


_action_table_name = "action"
_edition_table_name = "edition"
_sequence_table_name = "sequence"
_action_combination_table_name = "action_combination"
_plot_table_name = "plot"
default_database_path_suffix = ".apw"


def normalize_database_path(database_path: Path | str) -> Path:
    """
    Perform a number of updates to the path passed in

    - If the type is string, convert it to a Path
    - If the path does not have a suffix, add the default one
    """
    if isinstance(database_path, str):
        database_path = Path(database_path)

    # Only add the default suffix if the path doesn't already have one
    if len(database_path.suffix) == 0:
        database_path = database_path.with_suffix(default_database_path_suffix)

    return database_path


def dataset_exists(database_path: Path | str) -> bool:
    return normalize_database_path(database_path).exists()


def write_dataset(  # pylint: disable=too-many-locals, too-many-arguments
    actions: alias.Actions,
    sequences: alias.Sequences,
    tipping_point_by_action: alias.TippingPointByAction,
    colour_by_action: alias.ColourByAction,
    database_path: Path | str,
    *,
    overwrite: bool = True,
) -> None:
    """
    Save the information passed in to the database
    """
    assert len(colour_by_action) == len(actions), f"{colour_by_action} ↔ {actions}"

    database_path = normalize_database_path(database_path)

    if database_path.exists() and not overwrite:
        raise RuntimeError(f"Database {database_path} already exists")

    database_path.unlink(missing_ok=True)

    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.execute("PRAGMA ignore_check_constraints = 0")

    connection.execute(
        f"""
        CREATE TABLE {_action_table_name}
        (
            action_id INTEGER NOT NULL,
            name TEXT NOT NULL UNIQUE,

            PRIMARY KEY (action_id)
        )
        """
    )

    # edition_id is just a unique number identifying a unique action + edition combination
    connection.execute(
        f"""
        CREATE TABLE {_edition_table_name}
        (
            action_id INTEGER NOT NULL,
            edition_id INTEGER NOT NULL,

            FOREIGN KEY (action_id) REFERENCES {_action_table_name} (action_id),
            PRIMARY KEY (edition_id)
        )
        """
    )
    connection.execute(
        f"""
        CREATE TABLE {_sequence_table_name}
        (
            sequence_id INTEGER NOT NULL,
            from_edition_id INTEGER NOT NULL,
            to_edition_id INTEGER NOT NULL,
            tipping_point INTEGER NOT NULL CHECK (tipping_point >= 0),

            PRIMARY KEY (sequence_id),
            FOREIGN KEY (from_edition_id)
                REFERENCES {_edition_table_name} (edition_id),
            FOREIGN KEY (to_edition_id)
                REFERENCES {_edition_table_name} (edition_id)
        )
        """
    )
    connection.execute(
        f"""
        CREATE TABLE {_action_combination_table_name}
        (
            action_id INTEGER NOT NULL,
            combined_action_id INTEGER NOT NULL,

            UNIQUE (action_id, combined_action_id),
            FOREIGN KEY (action_id)
                REFERENCES {_action_table_name} (action_id),
            FOREIGN KEY (combined_action_id)
                REFERENCES {_action_table_name} (action_id)
        )
        """
    )
    connection.execute(
        f"""
        CREATE TABLE {_plot_table_name}
        (
            action_id INTEGER NOT NULL,
            colour TEXT NOT NULL,

            PRIMARY KEY (action_id),
            FOREIGN KEY (action_id) REFERENCES {_action_table_name} (action_id)
        )
        """
    )

    action_id_by_name = {
        action.name: action_id for action_id, action in enumerate(actions)
    }
    action_records = (
        {"action_id": action_id_by_name[action.name], "name": action.name}
        for action in actions
    )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_action_table_name}
            (
                action_id,
                name
            )
            VALUES
            (
                :action_id,
                :name
            )
            """,
            action_records,
        )

    # Sequences contain actions. Actions have a unique name. Actions with the same name are
    # the same action: they must have the same action_id. In the sequences, these actions must
    # be the same instance (have the same id()).
    # Actions with the same name, but with different id()'s are different instances of the
    # same action. They must be treated as being different editions. Actions with different
    # editions can be associated with different tipping points.

    # All unique Action instances, by name
    action_instances_by_name: dict[str, list[Action]] = {}

    # All unique Action instances, is some order
    action_instances: alias.Actions = []

    def add_action_instance(action):
        if action.name not in action_instances_by_name:
            action_instances_by_name[action.name] = [action]
            action_instances.append(action)
        elif action not in action_instances_by_name[action.name]:
            action_instances_by_name[action.name].append(action)
            action_instances.append(action)

    for sequence in sequences:
        for action in sequence:
            if isinstance(action, ActionCombination):
                for combined_action in action.actions:
                    add_action_instance(combined_action)

            add_action_instance(action)

    # Action edition ID by instance, in some order
    edition_id_by_instance = {
        action: edition_id for edition_id, action in enumerate(action_instances)
    }

    edition_records = (
        {
            "action_id": action_id_by_name[action.name],
            "edition_id": edition_id,
        }
        for action, edition_id in edition_id_by_instance.items()
    )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_edition_table_name}
            (
                action_id,
                edition_id
            )
            VALUES
            (
                :action_id,
                :edition_id
            )
            """,
            edition_records,
        )

    sequence_records = list(
        {
            "sequence_id": sequence_id,
            "from_edition_id": edition_id_by_instance[sequence[0]],
            "to_edition_id": edition_id_by_instance[sequence[1]],
            "tipping_point": tipping_point_by_action[sequence[1]],
        }
        for sequence_id, sequence in enumerate(sequences, start=1)
    )

    if len(sequences) > 0:
        root_actions = {
            action
            for action in tipping_point_by_action
            if action not in [sequence[1] for sequence in sequences]
        }
        assert (
            len(root_actions) == 1
        ), f"Expected a single root action, but found {root_actions}"
        root_action = root_actions.pop()

        sequence_records = [
            {
                "sequence_id": 0,
                "from_edition_id": edition_id_by_instance[root_action],
                "to_edition_id": edition_id_by_instance[root_action],
                "tipping_point": tipping_point_by_action[root_action],
            }
        ] + sequence_records

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_sequence_table_name}
            (
                sequence_id,
                from_edition_id,
                to_edition_id,
                tipping_point
            )
            VALUES
            (
                :sequence_id,
                :from_edition_id,
                :to_edition_id,
                :tipping_point
            )
            """,
            sequence_records,
        )

    # Action combination are actions that combine other actions. In the table we relate the id
    # of the action combination with the id's of the actions that are combined. In principle
    # any number (≥ 2) of actions can be combined into a single action combination.
    action_combination_records = []

    for action in actions:
        if isinstance(action, ActionCombination):
            for combined_action in action.actions:
                action_combination_records.append(
                    {
                        "action_id": action_id_by_name[action.name],
                        "combined_action_id": action_id_by_name[combined_action.name],
                    }
                )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_action_combination_table_name}
            (
                action_id,
                combined_action_id
            )
            VALUES
            (
                :action_id,
                :combined_action_id
            )
            """,
            action_combination_records,
        )

    plot_records = (
        {
            "action_id": action_id_by_name[action.name],
            "colour": rgba_to_hex(colour_by_action[action]),
        }
        for action in actions
    )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_plot_table_name}
            (
                action_id,
                colour
            )
            VALUES
            (
                :action_id,
                :colour
            )
            """,
            plot_records,
        )

    connection.close()


def read_dataset(  # pylint: disable=too-many-locals
    database_path: Path | str,
) -> tuple[
    alias.Actions, alias.Sequences, alias.TippingPointByAction, alias.ColourByAction
]:
    """
    Open the database and return the contents

    :return: Tuple of actions and sequences read
    """
    database_path = normalize_database_path(database_path)

    connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
    connection.execute("PRAGMA foreign_keys = 1")

    # TODO Use SQL for this?! We've got all relations set up. Use'm!

    action_data = list(
        connection.execute(
            f"""
            SELECT action_id, name
            FROM {_action_table_name}
            """
        )
    )

    action_name_by_id = {}

    for action_id, name in action_data:
        action_name_by_id[action_id] = name

    action_combination_data = list(
        connection.execute(
            f"""
            SELECT action_id, combined_action_id
            FROM {_action_combination_table_name}
            """
        )
    )
    combined_action_ids_by_action_id: dict[int, list[int]] = {}

    for action_id, combined_action_id in action_combination_data:
        combined_action_ids_by_action_id.setdefault(action_id, []).append(
            combined_action_id
        )

    action_by_id: dict[int, alias.Action] = {}

    # First add a regular action instance for all actions. This will keep the order as is.
    for action_id, action_name in action_name_by_id.items():
        action_by_id[action_id] = Action(action_name)

    # Now replace some of the actions by action combinations that combine regular actions
    for action_id, action_name in action_name_by_id.items():
        if action_id in combined_action_ids_by_action_id:
            combined_actions = [
                action_by_id[combined_action_id]
                for combined_action_id in combined_action_ids_by_action_id[action_id]
            ]
            action_by_id[action_id] = ActionCombination(action_name, combined_actions)

    edition_data = list(
        connection.execute(
            f"""
            SELECT action_id, edition_id
            FROM {_edition_table_name}
            """
        )
    )

    action_instance_by_edition: dict[tuple[str, int], Action] = {
        edition_id: copy.copy(action_by_id[action_id])
        for action_id, edition_id in edition_data
    }

    actions: alias.Actions = list(action_by_id.values())

    sequence_data = list(
        connection.execute(
            f"""
            SELECT sequence_id, from_edition_id, to_edition_id, tipping_point
            FROM {_sequence_table_name}
            """
        )
    )

    sequences = [
        (
            action_instance_by_edition[sequence_record[1]],
            action_instance_by_edition[sequence_record[2]],
        )
        for sequence_record in sequence_data
    ]

    if len(sequences) > 0:
        # One of the sequences relates the root action with itself. This is the one sequence which
        # we must remove from the collection.
        root_sequences = [
            (sequence[0], sequence[1])
            for sequence in sequences
            if sequence[0] == sequence[1]
        ]
        assert len(root_sequences) == 1, f"{root_sequences}"
        sequences.remove(root_sequences[0])

    to_actions = {sequence[1] for sequence in sequences}
    assert len(to_actions) == len(
        sequences
    ), "Detected sequences with converging actions which is not supported"

    tipping_point_by_action = {
        action_instance_by_edition[sequence_record[2]]: sequence_record[3]
        for sequence_record in sequence_data
    }

    plot_data = connection.execute(
        f"""
        SELECT action_id, colour
        FROM {_plot_table_name}
        """
    )

    colour_by_action = {
        action_by_id[plot_record[0]]: hex_to_rgba(plot_record[1])
        for plot_record in plot_data
    }

    for action in action_by_id.values():
        if not action in colour_by_action:
            colour_by_action[action] = default_node_colour()

    connection.close()

    assert len(colour_by_action) == len(actions), f"{colour_by_action} ↔ {actions}"

    return actions, sequences, tipping_point_by_action, colour_by_action
