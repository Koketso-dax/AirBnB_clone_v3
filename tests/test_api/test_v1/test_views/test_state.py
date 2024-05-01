#!/usr/bin/python3
'''testing the index route'''
import unittest
import json
from api.v1.app import *
from models.state import State
from models import storage


class TestStates(unittest.TestCase):
    '''test state'''
    def test_lists_states(self):
        '''test state GET route'''
        with app.test_client() as c:
            resp = c.get('/api/v1/states')
            self.assertEqual(resp.status_code, 200)
            resp2 = c.get('/api/v1/states/')
            self.assertEqual(resp.status_code, 200)

    def test_create_state(self):
        '''test state POST route'''
        with app.test_client() as c:
            resp = c.post('/api/v1/states/',
                          data=json.dumps({"name": "California"}),
                          content_type="application/json")
            self.assertEqual(resp.status_code, 201)

    def test_delete_state(self):
        '''test state DELETE route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            resp = c.get('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp.status_code, 200)
            resp1 = c.delete('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp1.status_code, 404)
            resp2 = c.get('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp2.status_code, 404)

    def test_get_state(self):
        '''test state GET by id route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            resp = c.get('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp.status_code, 200)

    def test_update_state(self):
        '''test state PUT route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            resp = c.put('api/v1/states/{}'.format(new_state.id),
                         data=json.dumps({"name": "Beckytopia"}),
                         content_type="application/json")
            self.assertEqual(resp.status_code, 200)

    def test_get_non_existing_state(self):
        """Test for get non-existing state case."""
        response = self.app.get('/api/v1/states/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_delete_non_existing_state(self):
        """Test for delete non-existing ..."""
        response = self.app.delete('/api/v1/states/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_create_state_missing_name(self):
        """Test for creating without a name"""
        data = {}
        response = self.app.post('/api/v1/states', json=data)
        self.assertEqual(response.status_code, 400)

    def test_create_state_invalid_json(self):
        """Test for invalid json create"""
        response = self.app.post('/api/v1/states', data='invalid_json')
        self.assertEqual(response.status_code, 400)

    def test_update_non_existing_state(self):
        """Test PUT non_existing state"""
        data = {'name': 'Updated State'}
        response = self.app.put('/api/v1/states/invalid_id', json=data)
        self.assertEqual(response.status_code, 404)

    def test_update_state_invalid_json(self):
        """Test updating with invalid json."""
        response = self.app.put(f'/api/v1/states/{self.state.id}', data='invalid_json')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
