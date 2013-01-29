import unittest

class warmerTestCase(unittest.TestCase):
    def runTest(self):
        url = 'http://localhost'
        headers = {
            'test-header' : 1,
            'host' : 'foo.example.com'
        }
        results = warmer.warm_url(url, headers)


