import calendar
from datetime import date, timedelta

from src.db_utils import *


# Test classes to be used for insertion
class_biology = {
    COLUMN_CLASS_NAME: 'Biology',
    COLUMN_START_TIME: '9:45 AM',
    COLUMN_END_TIME: '10:45 AM',
    COLUMN_DAYS: [
        'Monday',
        'Wednesday',
        'Friday'
    ]
}

class_psychology = {
    COLUMN_CLASS_NAME: 'Psychology',
    COLUMN_START_TIME: '2:30 PM',
    COLUMN_END_TIME: '4:00 PM',
    COLUMN_DAYS: [
        'Tuesday',
        'Thursday'
    ]
}

class_astronomy = {
    COLUMN_CLASS_NAME: 'Astronomy',
    COLUMN_START_TIME: '7:30 PM',
    COLUMN_END_TIME: '8:45 PM',
    COLUMN_DAYS: [
        'Wednesday',
        'Friday'
    ]
}


# noinspection PyBroadException
def update_item(class_name, update_time=False, append_date=False, delete_date=False):
    try:
        if update_time:
            table.update_item(
                Key={COLUMN_CLASS_NAME: class_name},
                UpdateExpression=f'SET {COLUMN_START_TIME} = :value',
                ExpressionAttributeValues={':value': '3:45 AM'}
            )
        if append_date:
            table.update_item(
                Key={COLUMN_CLASS_NAME: class_name},
                UpdateExpression=f'SET {COLUMN_DAYS} = list_append(days, :value)',
                ExpressionAttributeValues={':value': ['Monday']}
            )
        if delete_date:
            table.update_item(
                Key={COLUMN_CLASS_NAME: class_name},
                UpdateExpression=f'REMOVE {COLUMN_DAYS}[2]',
                ExpressionAttributeValues={':value': 'Monday'}
            )
        print(f'Successfully updated {class_name}')
    except Exception as e:
        print(f'Error: {e}')


def print_formatted_list_of_all_classes():
    today = calendar.day_name[date.today().weekday()].lower()
    tomorrow = calendar.day_name[(date.today() + timedelta(days=1)).weekday()].lower()
    yesterday = calendar.day_name[(date.today() + timedelta(days=-1)).weekday()].lower()
    print(f'Yesterday was: {yesterday}')
    print(f'Today is: {today}')
    print(f'Tomorrow is: {tomorrow}')
    pass


if __name__ == '__main__':
    # insert_item(class_astronomy)
    # update_item(class_psychology[COLUMN_CLASS_NAME], delete_date=True)
    # delete_item(class_astronomy[COLUMN_CLASS_NAME])
    pass
