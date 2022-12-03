import unittest
from unittest import TestCase
from main import app
import base64
from flask import request
from datetime import datetime

class MyTest(TestCase):
    client = app.test_client()

    def create_app(self):
        app.config['TESTING'] = True
        return app

class ApiTests(TestCase):
    client = app.test_client()

    def test_user_wrong_data(self):
        test_user_json = {
            "username":"tester1",
            "firstname":"Test1",
            "lastname":"Testivych",
            "email":"test1@gmail",
            "password":"123456789",
            "phone":"0989812544",
        }

        r = self.client.post('/user', json=test_user_json)

        assert r.status_code == 400
        assert r.json['Error'] == "Wrong Data!"

    def test_user_login_wrong(self):
        valid_credentials = base64.b64encode(b"tester1:12345678910").decode("utf-8")
        r = self.client.post('/user/login', headers={"Authorization": "Basic " + valid_credentials})

        assert r.status_code == 404
        assert r.json['Error'] == "User not found"

        valid_credentials = base64.b64encode(b"vladislove:12345678910").decode("utf-8")
        r = self.client.post('/user/login', headers={"Authorization": "Basic " + valid_credentials})

        assert r.status_code == 401
        assert r.json['Error'] == "Wrong password"

    def test_user_login_username_wrong(self):
        valid_credentials = base64.b64encode(b"vladislove123:12345678910").decode("utf-8")
        r = self.client.post('/user/login', headers={"Authorization": "Basic " + valid_credentials})

        assert r.status_code == 404
        assert r.json['Error'] == "User not found"

    def test_user_get(self):
        r = self.client.get('/user/noname', headers={'Authorization': f"Bearer {self.login_admin()}"})
        assert r.status_code == 401

    def test_get_event(self):
        r = self.client.get('/event/100120102')
        assert r.status_code == 404
        assert r.json['Error'] == "Event not found"

    def test_get_event_tickets(self):
        r = self.client.get('/event/10016545/tickets')
        assert r.status_code == 200

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

        r = self.client.post('/event', json={}, headers={'Authorization': f"Bearer {token}"})
        assert r.status_code == 403
        assert r.json['msg'] == "Admins only!"

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
            'name': 'New Year party',
            'address': 'Ukraine',
            'datatime': '2021-12-05 12:15:12',
            'tickets_count': 300
        }

        auth_header = {'Authorization': f"Bearer {self.login_admin()}"}

        r = self.client.post('/event', json=test_event_json, headers=auth_header)

        assert r.status_code == 400
        assert r.json['Error']== "This is not proper date"

        test_event_json = {
            'name':'New Year party',
            'address':'Ukraine',
            'datatime':'2022-12-05 12:15:12',
            'tickets_count':300
        }

        auth_header = {'Authorization': f"Bearer {self.login_admin()}"}

        r = self.client.post('/event', json=test_event_json, headers=auth_header)

        assert r.status_code == 200

        _id = int(r.json['id'])

        r = self.client.get(f'/event/{_id}')
        assert r.status_code == 200

        ticket={
            'seat':1,
            'type': 'reserved',
            'user_id': 1,
            'event_id': _id
        }

        r = self.client.post('/ticket', json=ticket, headers=auth_header)
        assert r.status_code == 200

        _ticket_id = r.json['id']

        r = self.client.post('/ticket', json=ticket, headers=auth_header)

        assert r.status_code == 409

        ticket2 = {
            'seat': 11,
            'type': 'res',
            'user_id': 1,
            'event_id': _id
        }

        r = self.client.post('/ticket', json=ticket2, headers=auth_header)

        assert r.status_code == 409

        r = self.client.get('/user/vladislove/tickets', headers=auth_header)
        assert r.status_code == 200

        r = self.client.get(f'/event/{_id}/tickets', headers=auth_header)
        assert r.status_code == 200

        ticket_upd={
            'seat':2
        }

        r = self.client.put(f'/ticket/{_ticket_id}',json=ticket_upd, headers=auth_header)
        assert r.status_code == 200

        r = self.client.delete(f'/ticket/{_ticket_id}', headers=auth_header)
        assert r.status_code == 200

        test_event_upd_json = {
            "datatime": "2022-12-31 10:00:00",
        }

        r = self.client.put(f'/event/{_id}', json=test_event_upd_json, headers=auth_header)
        assert r.status_code == 200

        r = self.client.put(f'/event/12301023', json=test_event_upd_json, headers=auth_header)
        assert r.status_code == 404

        r = self.client.delete(f'/event/{_id}', headers=auth_header)
        assert r.status_code == 200


    def login_admin(self):
        valid_credentials = base64.b64encode(b"vladislove:12345678").decode("utf-8")
        r = self.client.post('/user/login', headers={"Authorization": "Basic " + valid_credentials})

        token = str(r.json['access_token'])
        return token