import os
import unittest
import tempfile
import json
import re

import app

class FlaskrTestCase(unittest.TestCase):

    def get_obj(self, response):
        """
        Utility method to convert flask response to JSON.
        Seems like this should not be necessary.
        """
        # Convert response to string and remove leading b indicating byte stream
        tmp =  re.sub("^b", "", str(response.data))
        # remove leading and trailing single quote
        tmp = re.sub("^'|'$", "", str(tmp))
        # remove '\n' at end
        tmp = re.sub("\\\\n$", "", tmp)
        # convert json to object and return
        return json.loads(tmp)

    def setUp(self):
        # self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        # with flaskr.app.app_context():
        #     flaskr.init_db()
    #
    # def tearDown(self):
    #     os.close(self.db_fd)
    #     os.unlink(flaskr.app.config['DATABASE'])


    def test_get(self):
        rv = self.app.get('/')
        # import IPython;IPython.embed()
        self.assertEqual(200, rv.status_code)
        self.assertEqual(dict(hello='world'), self.get_obj(rv))

    def test_post(self):
        rv = self.app.post('/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(dict(goodbye='world'), self.get_obj(rv))


if __name__ == '__main__':
    unittest.main()
