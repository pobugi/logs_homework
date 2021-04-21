import requests
from .merge_sort import merge_sort


def get_logs(date):

    url_base = "http://www.dsdev.tech/logs/{}"
    url = url_base.format(date)

    bulk_data = requests.get(url).json()

    if bulk_data['error']:
        return bulk_data

    list_of_logs = bulk_data['logs']
    result = merge_sort(list_of_logs, 'created_at')

    return result
