import unittest
import requests
import json
from app import app, db, Products

class testApi(unittest.TestCase):
    URL = "http://127.0.0.1:5000"

    data = {
        'name': 'test_potato',
        'arrival_data': '15.07.1995',
        'category': 'vegies',
        'country': 'ua',
        'price': '20'
    }

    update_data = {
        'name': 'test_potato',
        'category': 'Vegetables',
        'price': '22'
    }


    def test1(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        print("Test 1 completed")

    def test2(self):
        resp = requests.post(self.URL + '/json_add', json=self.data)
        self.assertEqual(resp.status_code, 201)

        print("test 2 done")


    def test3(self):
        test_id = Products.query.filter_by(name='test_potato').all()
        for id in test_id:
            resp = requests.put(self.URL + '/json_update/' + str(id.id) + '/', json=self.update_data)
            self.assertEqual(resp.status_code, 204)

        print("Test 3 done")


    def test4(self):
        test_id = Products.query.filter_by(name='test_potato').all()
        for id in test_id:
            resp = requests.delete(self.URL + '/json_delete/' + str(id.id) + '/')
            self.assertEqual(resp.status_code, 204)

        print("Test 4 done")


if __name__ == "__main__":
    tester = testApi()


    tester.test1()
    tester.test2()
    tester.test3()
    tester.test4()
