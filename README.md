# skill-for-github
Connecting your github w/ alexa voice services

Some interactions supported are:
 - alexa ask github to get account info
 - alexa ask github to get my organizations
 - alexa ask github what's new
 - alexa ask github to list my repos

Testing
 - git clone https://github.com/fugue/emulambda/
 - pip install -e emulambda
 - run service simulator and use utterance "open github".
 - grab "accessToken" from lambda request json and store in testing.ini
 - run "python setup.py test"
