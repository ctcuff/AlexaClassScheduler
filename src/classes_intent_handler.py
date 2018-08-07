"""
This contains methods for handling intents that AREN'T Alexa's built in intents
"""
import calendar
from datetime import date

from src.response_utils import *
from src.db_utils import *

VALID_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
WEEK_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
WEEKENDS = ['saturday', 'sunday']


def list_classes_for_today(day=None):
    """
    Search the table and print out only the classes that the user has either today or for a given day.
    If day is None, then today's date will be used
    """
    search_date = calendar.day_name[date.today().weekday()].lower() if day is None else day.lower()
    card_title = f'Schedule for {search_date}'
    classes = get_classes_for_date(search_date)
    for clazz in classes:
        print(clazz)
    # Check to see how many classes we have so we can build a properly formatted response
    if len(classes) == 0:
        response = "You don't have any classes today" if day is None \
            else f"You don't have any classes on {search_date}"
    elif len(classes) == 1:
        clazz = classes[0]
        response = f'You only have {clazz[COLUMN_CLASS_NAME]} today, it starts at {clazz[COLUMN_START_TIME]} ' \
                   f'and ends at {clazz[COLUMN_END_TIME]}' if day is None \
            else f'You only have {clazz[COLUMN_CLASS_NAME]} on {search_date}, it starts at {clazz[COLUMN_START_TIME]} ' \
                 f'and ends at {clazz[COLUMN_END_TIME]}'
    elif len(classes) > 1:
        response = f'You have {len(classes)} classes today, ' if day is None \
            else f'You have {len(classes)} classes on {search_date}, '
        for i in range(len(classes) - 1):
            clazz = classes[i]
            response += f'{clazz[COLUMN_CLASS_NAME]}, which starts at {clazz[COLUMN_START_TIME]}, '
        clazz = classes[len(classes) - 1]
        response += f'and {clazz[COLUMN_CLASS_NAME]}, which starts at {clazz[COLUMN_START_TIME]}'
    else:
        response = 'An error occurred while retrieving your schedule'
    return build_response({}, build_speechlet_response(card_title, response, None, True))


def add_class_title(intent):
    card_title = "Class Schedule"
    session_attributes = {}
    if 'class' in intent['slots']:
        clazz = intent['slots']['class']['value']
        session_attributes = {'class': clazz}
        if not is_class_in_database(clazz):
            response = f"Alright, I'll add {clazz} to your schedule, what time does {clazz} start"
        else:
            response = f"{clazz} is already in your schedule, you can continue to update it or say cancel to stop. " \
                       f"What time does {clazz} start"
    else:
        response = 'An unexpected error has occurred'
    return build_response(session_attributes, build_speechlet_response(card_title, response, None, False))


def add_class_start_or_end_time(intent, session):
    card_title = "Class Schedule"
    session_attributes = {}
    if 'time' in intent['slots']:
        clazz = session['attributes']['class']
        session_attributes['class'] = clazz
        time = intent['slots']['time']['value']
        # If the start time for the class isn't in the current session attributes,
        # that means that Alexa has asked for a start time
        if 'start_time' not in session.get('attributes', {}):
            session_attributes['start_time'] = format_24_hour_time(time)
            response = f"What time does {clazz} end"
        # If the start time for the class is already in the current session attributes,
        # that means that Alexa has asked for a end time
        else:
            session_attributes['start_time'] = session['attributes']['start_time']
            session_attributes['end_time'] = format_24_hour_time(time)
            response = f'On what days does {clazz} occur'
    else:
        response = 'An unexpected error has occurred'
    return build_response(session_attributes, build_speechlet_response(card_title, response, None, False))


def add_class_days(intent, session):
    # TODO: Probably check for errors???
    card_title = "Class Schedule"
    session_attributes = {}

    # Get all the current session attributes
    clazz = session['attributes']['class']
    start_time = session['attributes']['start_time']
    end_time = session['attributes']['end_time']
    days = intent['slots']['days']['value']

    # Make sure the session attributes we retrieved above carry on to the next session,
    # this way, the user can say 'yes' to add this class to the database
    session_attributes['class'] = clazz
    session_attributes['start_time'] = start_time
    session_attributes['end_time'] = end_time
    session_attributes['days'] = days
    response = f"Alright, you've told me that {clazz} starts at {start_time}, ends at {end_time}, and occurs " \
               f"on {days}. Is this correct"
    return build_response(session_attributes, build_speechlet_response(card_title, response, None, False))


def add_class_to_database(session):
    card_title = "Class Schedule"
    # card_text = None
    session_attributes = {}
    class_name = session['attributes']['class']
    start_time = session['attributes']['start_time']
    end_time = session['attributes']['end_time']
    days_string = session['attributes']['days']

    session_attributes['class'] = class_name
    session_attributes['start_time'] = start_time
    session_attributes['end_time'] = end_time
    session_attributes['days'] = days_string

    days = []
    # Remove any punctuation if there is any and convert
    # plural/capital dates (Mondays) to lowercase singular dates (monday)
    for day in days_string.replace('.', '').split():
        if day.lower().endswith('s'):
            # Get the date but without the 's'
            if day[:-1].lower() in VALID_DAYS:
                days.append(day[:-1].lower())
        elif day.lower() in VALID_DAYS:
            days.append(day.lower())

    clazz = {
        COLUMN_CLASS_NAME: class_name,
        COLUMN_START_TIME: start_time,
        COLUMN_END_TIME: end_time,
        COLUMN_DAYS: days
    }
    # Check if the class was already in the database before we add it, this way, we can tell
    # the user that the class was updated instead of added if it already existed
    was_class_already_in_database = is_class_in_database(class_name)
    success, error = insert_class(clazz)
    if success:
        response = f"Ok, I've updated {class_name}" if was_class_already_in_database \
            else f"Ok, I've added {class_name} to your schedule"
    else:
        response = f'An error occurred while updating {class_name}' if was_class_already_in_database \
            else f'An error occurred while adding {class_name} to your schedule'
        card_title = 'An error occurred'
    return build_response(session_attributes, build_speechlet_response(card_title, response, None, True))


def remove_class_with_confirmation(intent):
    """
    This doesn't actually remove a class, it will simply prompt Alexa to confirm if the user
    wants to remove a class from their schedule (provided it exists). If the user says yes,
    remove_class(session) will be called
    """
    card_title = "Class Schedule"
    session_attributes = {}
    should_session_end = False
    if 'classToRemove' in intent['slots']:
        clazz = intent['slots']['classToRemove']['value']
        session_attributes = {'classToRemove': clazz}
        if is_class_in_database(clazz):
            response = f"Are you sure you want to remove {clazz} from your schedule"
        else:
            response = f"You don't have {clazz} in your schedule"
            should_session_end = True
    else:
        response = 'An unexpected error has occurred'
        should_session_end = True
    return build_response(session_attributes, build_speechlet_response(card_title, response, None, should_session_end))


def remove_class(session):
    card_title = "Class Schedule"
    session_attributes = {}
    if 'classToRemove' in session.get('attributes', {}):
        clazz = session['attributes']['classToRemove']
        success, error = delete_class(clazz)
        if success:
            response = f"I've removed {clazz} from your schedule"
        else:
            response = 'An unexpected error occurred while removing your class'
            card_title = str(error)
    else:
        response = 'An unexpected error has occurred'
    return build_response(session_attributes, build_speechlet_response(card_title, response, None, True))
