def get_metric_value_by_name(metric_data, metric_name):
    """
    Retrieves a MetricValue object from metric_data of an Action by the name of the Metric object.

    :param metric_data: The Metric_data dict for an Action, Sequence or ActionInstance to query.
    :param metric_name: The name of the Metric to search for.
    :return: The corresponding MetricValue, or None if not found.
    """
    for metric, value in metric_data.items():
        if metric.name == metric_name:
            return value
    return None
