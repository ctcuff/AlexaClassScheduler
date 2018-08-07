from datetime import timedelta

from src.classes_intent_handler import *


# --------------- Main handler ------------------
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


# --------------- Events ------------------
def on_session_started(session_started_request, session):
    """ Called when the session starts """


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """
    # Dispatch to the skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Intents we've defined
    if intent_name == 'ViewClassesIntent':
        return list_classes_for_today()

    elif intent_name == 'ViewTomorrowClasses':
        tomorrow = calendar.day_name[(date.today() + timedelta(days=1)).weekday()].lower()
        return list_classes_for_today(day=tomorrow)

    elif intent_name == 'ViewClassesForDate':
        day = intent['slots']['day']['value']
        return list_classes_for_today(day=day.lower())

    elif intent_name == 'AddClassIntent':
        return add_class_title(intent)

    elif intent_name == 'SetStartEndTime':
        return add_class_start_or_end_time(intent, session)

    elif intent_name == 'SetClassDays':
        return add_class_days(intent, session)

    elif intent_name == 'RemoveClassIntent':
        return remove_class_with_confirmation(intent)

    # Built in intents
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or intent_name == 'AMAZON.NoIntent':
        return handle_session_end_request()

    elif intent_name == "AMAZON.YesIntent":
        # The user said yes but they did so after Alexa asked for confirmation in removing a class
        if 'classToRemove' in session.get('attributes', {}):
            return remove_class(session)
        else:
            return add_class_to_database(session)
    else:
        speech_output = "I'm not sure I understood that"
        card_title = speech_output
        return build_response({}, build_speechlet_response(card_title, speech_output, None, True))


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Is not called when the skill returns should_end_session=true """


def get_welcome_response():
    card_title = "Welcome"
    speech_output = 'Welcome to class scheduler. ' \
                    'You can ask me to add a class to your schedule or read your schedule for the day or week'
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm sorry, I didn't understand."
    return build_response({}, build_speechlet_response(card_title, speech_output, reprompt_text, False))


def handle_session_end_request():
    # TODO: Check session attributes to determine if the user cancelled during class scheduling
    card_title = "Canceled"
    speech_output = "Alright"
    # Setting this to true ends the session and exits the skill.
    return build_response({}, build_speechlet_response(card_title, speech_output, None, True))
