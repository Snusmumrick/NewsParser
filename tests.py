import unittest
from load import *
from app import checkParams

class TestLoadModule(unittest.TestCase):

    def test_getInfoFromSite(self):
        self.assertEqual(type(getInfoFromSite()),type([]))

    def test_checkParams(self):
        with self.assertRaises(Exception) as context:
            checkParams('date',1,2)
        self.assertTrue('Wrong order param' in str(context.exception))

        with self.assertRaises(Exception) as context:
            checkParams('id',-1,2)
        self.assertTrue('Limit should be in 0' in str(context.exception))

        with self.assertRaises(Exception) as context:
            checkParams('id',100,2)
        self.assertTrue('Limit should be in 0' in str(context.exception))

        with self.assertRaises(Exception) as context:
            checkParams('id',"hekko",2)
        self.assertTrue('Limit should be integer' in str(context.exception))

    def test_posts(self):
        rv = self.app.get('/')
        assert 'Unbelievable.  No entries here so far' in rv.data
if __name__ == '__main__':
    unittest.main()
