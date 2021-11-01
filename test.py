import unittest
import requests
import json
from app import app, db

class testApi(unittest.TestCase):
    URL = "http://127.0.0.1:5000"


    def test1(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        print("Test 1 completed")

    def test2(self):
        resp = requests.post('/add_product', data={'name':'potato', 'arrival_data':'15.07.1995', 'category':'vegies', 'country':'ua', 'price':'20'})
        self.assertEquals(response.status_code, 200)

if __name__ == "__main__":
    tester = testApi()


    tester.test1()
    tester.test2()