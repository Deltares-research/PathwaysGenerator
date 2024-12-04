from ..app.model.metric import MetricValue


def evaluate_criterion(metrics: list[MetricValue], num_needed: int):
    """
    Evaluates a single metric across multiple actions in a sequence.

    :param metrics: List of MetricValue objects from the sequence.
    :param num_needed: integer to specify number of actions in Sequence considered for evaluation
    :return: A MetricValue object representing the combined evaluation.
    """
    relevant_metrics = metrics[:num_needed]
    if all(isinstance(metric.value, (int, float)) for metric in relevant_metrics):
        # Combine numeric values by summing them
        value = sum(metric.value for metric in relevant_metrics)
        return MetricValue(
            value=value,
            is_estimate=any(metric.is_estimate for metric in relevant_metrics),
        )

    raise ValueError(
        "Inconsistent data types in metrics: must be all strings or all numeric."
    )
