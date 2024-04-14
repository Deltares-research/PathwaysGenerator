from .. import alias
from . import binary, text


def read_dataset(
    basename_pathname: str,
) -> tuple[
    alias.Actions, alias.Sequences, alias.TippingPointByAction, alias.ColourByAction
]:
    """
    Read a dataset and return the contents

    :raises RuntimeError: In case an error occurred

    This function supports reading information from both the binary and text formats. First
    the binary format is tried, and when that fails the text format is tried. If both binary
    and text formatted datasets exist with the same name, then the contents from the binary
    one are returned.
    """

    binary_dataset_exists = binary.dataset_exists(basename_pathname)

    try:
        if binary.dataset_exists(basename_pathname):
            # pylint: disable-next=unused-variable
            actions, sequences, tipping_point_by_action, colour_by_action = (
                binary.read_dataset(basename_pathname)
            )
        else:
            # pylint: disable-next=unused-variable
            actions, sequences, tipping_point_by_action, colour_by_action = (
                text.read_dataset(basename_pathname)
            )
    except Exception as exception:
        if binary_dataset_exists:
            message = f"Error while reading binary dataset {basename_pathname}"
        else:
            message = (
                f"Error while reading text dataset {basename_pathname}. "
                "(First tried reading a binary dataset with that name "
                "but it does not exist.)"
            )
        raise RuntimeError(message) from exception

    return actions, sequences, tipping_point_by_action, colour_by_action
