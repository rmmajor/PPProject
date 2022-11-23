import unittest
from unittest import TestCase
from main import app
import base64
from flask import request

class MyTest(TestCase):
    client = app.test_client()

    def create_app(self):
        app.config['TESTING'] = True
        return app

class ApiTests(TestCase):
    client = app.test_client()


    def test_user(self):
        test_user_json = {
            "username":"tester1",
            "firstname":"Test1",
            "lastname":"Testivych",
            "email":"test1@gmail.com",
            "password":"123456789",
            "phone":"0989812544",
        }

        r = self.client.post('/user', json=test_user_json)

        assert r.status_code == 200

        valid_credentials = base64.b64encode(b"tester1:123456789").decode("utf-8")
        r = self.client.post('/user/login', headers={"Authorization": "Basic " + valid_credentials})

        token = str(r.json['access_token'])

        test_user_upd_json = {
            "username": "tester1Updated",
            "firstname": "Test1Updated",
        }

        r = self.client.put('/user/tester1', json=test_user_upd_json, headers={'Authorization': f"Bearer {token}"})

        assert r.status_code == 200

        valid_credentials = base64.b64encode(b"tester1Updated:123456789").decode("utf-8")
        r = self.client.post('/user/login', headers={"Authorization": "Basic " + valid_credentials})

        token = str(r.json['access_token'])

        r = self.client.delete('/user/tester1Updated', headers={'Authorization': f"Bearer {token}"})

        assert r.status_code == 200

    def test_events(self):
        test_event_json = {
            'name':'New Year party',
            'address':'Ukraine',
            'datatime':'2022-12-05 12:15:12',
            'tickets_count':300
        }

        

        r = self.client.post('/event', json=test_event_json, headers=self.auth_header)

        print(r.json)

        assert r.status_code == 200

        _id = int(r.json['id'])

        r = self.client.get(f'/event/{_id}')
        assert r.status_code == 200

        test_event_upd_json = {
            "datatime": "2022-12-31 10:00:00",
        }

        r = self.client.put(f'/event/{_id}', json=test_event_upd_json, headers=self.auth_header)
        assert r.status_code == 200

        r = self.client.delete(f'/event/{_id}', headers=self.auth_header)
        assert r.status_code == 200

    def login_admin(self):
        valid_credentials = base64.b64encode(b"vladislove:12345678").decode("utf-8")
        r = self.client.post('/user/login', headers={"Authorization": "Basic " + valid_credentials})

        token = str(r.json['access_token'])
        return token