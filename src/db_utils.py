import boto3
from boto3.dynamodb.conditions import Key

from src.keys import *

REGION = 'us-west-2'
TABLE_NAME = 'Classes'
COLUMN_CLASS_NAME = 'class_name'
COLUMN_START_TIME = 'start_time'
COLUMN_END_TIME = 'end_time'
COLUMN_DAYS = 'days'

_session = boto3.Session(aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
_dynamodb = _session.resource('dynamodb', region_name='us-west-2')
table = _dynamodb.Table('Classes')


# Classes are stored in the database like this:
# {
#     'class_name': 'Biology',
#     'start_time': '9:45',
#     'end_time': '10:45',
#     'days': [
#         'monday',
#         'wednesday',
#         'friday'
#     ]
# }


def insert_class(clazz):
    try:
        table.put_item(Item=clazz)
        return True, None
    except Exception as e:
        return False, e


def delete_class(class_name):
    try:
        table.delete_item(Key={COLUMN_CLASS_NAME: class_name})
        return True, None
    except Exception as e:
        return False, str(e)


# noinspection PyBroadException
def get_class(class_name):
    try:
        item = table.get_item(Key={COLUMN_CLASS_NAME: class_name})
        return item['Item']
    except Exception:
        # The class doesn't exist
        return None


# noinspection PyBroadException
def get_all_classes():
    try:
        item = table.scan()
        return item['Items']
    except Exception:
        return None


def get_classes_for_date(search_date):
    classes = get_all_classes()
    if classes is None:
        return None
    return [clazz for clazz in classes if search_date in clazz['days']]


def is_class_in_database(class_name):
    items = table.query(KeyConditionExpression=Key(COLUMN_CLASS_NAME).eq(class_name))
    return items['Items']
