
from __future__ import print_function
from github import Github


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "I connect to your git hub account. " \
                    "ask me to list your repos, " \
                    "or what's new."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask what's new."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "OK"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_notifications(intent, session):
    """ queries github for recent events on your account
    """

    card_title = intent['name']
    session_attributes = {}
    reprompt_text = ''
    should_end_session = True

    g = Github(session['user']['accessToken'])
    events = g.get_user().get_notifications()
    num_events = 0
    event_strings = []
    for evt in events:
        num_events += 1
        if num_events < 5:
            event_strings.append(evt.subject.type+' for '+evt.repository.name+', '+evt.subject.title)

    if num_events > 0:
        speech_output = \
            'You have {0} notifications.'.format(num_events) + ', here are the first 5. ' + \
            ', '.join(event_strings)
        reprompt_text = ''
    else:
        speech_output = "Nothing new since last time you asked."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_repos(intent, session):
    session_attributes = {}
    reprompt_text = None

    g = Github(session['user']['accessToken'])
    repos = g.get_user().get_repos()
    index = 0
    if 'attributes' in session and 'index' in session['attributes']:
        index = int(session['attributes']['index'])
    num_repos = 0
    repo_strings = []
    for rep in repos:
        num_repos += 1
        if num_repos >= index and num_repos < (index + 5):
            repo_strings.append(rep.name)
    # TODO: handle end of list, by ending the session
    if num_repos > 0:
        if index == 0:
            speech_output = 'You have {0} repos. The first 5 are '.format(num_repos) + \
                ', '.join(repo_strings) + 'Shall I continue?'
        else:
            speech_output = \
                ','.join(repo_strings) + ' Shall I continue?'
        reprompt_text = 'Should I list more?'
        should_end_session = False
        session_attributes['index'] = index + 5
        session_attributes['intent'] = 'GetRepos'
    else:
        speech_output = "You don't have any repos in this account."
        should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def get_acct_info(intent, session):
    session_attributes = {}
    reprompt_text = None
    should_end_session = True

    g = Github(session['user']['accessToken'])
    u = g.get_user()
    speech_output = \
        'You are {0}. You have {1} public repose, {2} followers and are following {3}.'. \
        format(u.name, u.public_repos, u.followers, u.following)

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def get_orgs(intent, session):
    session_attributes = {}
    reprompt_text = None
    should_end_session = True

    g = Github(session['user']['accessToken'])
    orgs = g.get_user().get_orgs()
    num_orgs = 0
    org_strings = []
    for org in orgs:
        num_orgs += 1
        org_strings.append(org.url[org.url.rfind('/')+1:])
    if num_orgs > 0:
        speech_output = \
            'You belong to these organizations. ' + ','.join(org_strings)
    else:
        speech_output = "You don't have any organizations in this account."

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print(
        "on_session_started requestId=" +
        session_started_request['requestId'] +
        ", sessionId=" + session['sessionId']
    )


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.YesIntent":
        if session['attributes']['intent'] == 'GetRepos':
            return get_repos(intent, session)
    elif intent_name == "GetNotifications":
        return get_notifications(intent, session)
    elif intent_name == "GetRepos":
        return get_repos(intent, session)
    elif intent_name == "GetOrganizations":
        return get_orgs(intent, session)
    elif intent_name == "GetAcctInfo":
        return get_acct_info(intent, session)
    elif intent_name == "AMAZON.NoIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    # if no amazon token, return a LinkAccount card

    if 'accessToken' not in event['session']['user']:
        return build_response({}, {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'to start using this skill, please use the companion app to authenticate on github',
            },
            'card': {
                'type': 'LinkAccount',
            },
            'shouldEndSession': False
        })

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
