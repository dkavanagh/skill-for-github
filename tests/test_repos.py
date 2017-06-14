
import json
import unittest

import emulambda

from githubskill import lambda_handler

class RepoTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_repos(self):
        event = {}
        with open('tests/intent-get-repos.json', 'r') as intent_file:
            event_json=intent_file.read().replace('\n', '')
            event = json.loads(event_json)
        result, exec_clock = emulambda.invoke_lambda(lambda_handler, event, None, 300, '')
        print('result = '+str(result))
        self.assertEqual(result['response']['reprompt']['outputSpeech']['text'], 'Should I list more?')
