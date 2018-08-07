"""
Helpers that build all of the responses
"""

card_title_prefix = 'Class Scheduler'


def build_speechlet_response(title, output, reprompt_text, should_end_session, card_text=None):
    """
    Build a speechlet JSON representation of the title, output text,
    reprompt text & end of session

    :param title: The title of the card (used in the iOS/Android companion app)
    :param output: The text Alexa will speak
    :param reprompt_text: The text Alexa will speak after the user tells Alexa something
    :param should_end_session: Whether or not this session will end after Alexa finishes talking
    :param card_text: The text body of the card (used in the iOS/Android companion app)
    :return: A JSON representation of the speechlet
    """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': f'{card_title_prefix} - {title}',
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    """
    Build the full response JSON from the speechlet response
    """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def format_24_hour_time(time):
    """
    Takes a time such as 23:59 and returns 11:59
    """
    hour = int(time[:2])
    # 00:30 => 12:30
    if hour == 0:
        return '12' + time[2:]
    # 3:30 => 3:30
    if 1 <= hour <= 12:
        return str(time)
    # 22:50 => 10:50
    if hour > 12:
        hour -= 12
        return str(hour) + time[2:]
