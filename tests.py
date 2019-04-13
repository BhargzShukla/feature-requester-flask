import json
import unittest

from copy import deepcopy
from datetime import datetime

from dateutil.relativedelta import relativedelta

from feature_requester_app import app as app
from feature_requester_app.models import (
    db,
    Client,
    ProductArea,
    FeatureRequest
)
from flask_fixtures import FixturesMixin


app.config.from_object('feature_requester_app.config.TestingConfiguration')


class FeatureRequestTestCase(unittest.TestCase, FixturesMixin):
    fixtures = ['clients.json', 'product_areas.json']
    app, db = app, db
    test_data = {
        'title': 'Test request',
        'description': 'Test request feature description',
        'client': 1,
        'client_priority': 1,
        'product_area': 1,
        'target_date': str(datetime.utcnow().date())
    }

    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_clients_initial_data(self):
        u"""
        Test for initial clients data loaded
        from the 'clients.json' fixture.
        """
        clients = Client.query.all()
        assert len(clients) == Client.query.count() == 3

    def test_product_area_initial_data(self):
        u"""
        Test for initial product_area data loaded
        from the 'product_areas.json' fixture.
        """
        product_areas = ProductArea.query.all()
        assert len(product_areas) == ProductArea.query.count() == 4

    def test_add_feature_request_no_data(self):
        u"""
        Test adding a new feature request with no input data.
        """
        response = self.app.post('api/feature_requests/add/', data=dict())
        response_data = json.loads(response.get_data())
        assert response_data['message'] == 'No input provided'

    def test_add_feature_request_valid_data(self):
        u"""
        Test adding a new feature request with valid input data.
        """
        response = self.app.post(
            'api/feature_requests/add/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Feature request added'

    def test_add_feature_request_invalid_title(self):
        u"""
        Test adding a new feature request with invalid "title" data.
        """
        test_data = deepcopy(self.test_data)
        test_data['title'] = 'less'
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['title'][0] == \
            'Length must be between 5 and 255.'

    def test_add_feature_request_past_target_date(self):
        u"""
        Test adding a new feature request with invalid "target_date"
        data (value < now).
        """
        test_data = deepcopy(self.test_data)
        now = datetime.utcnow().date()
        test_data['target_date'] = str(now - relativedelta(months=1))
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['target_date'][0] == \
            'Target date must be in the future'

    def test_add_feature_request_negative_client_priority(self):
        u"""
        Test adding a new feature request with invalid "client_priority"
        data (value < 0).
        """
        test_data = deepcopy(self.test_data)
        test_data['client_priority'] = -1
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['client_priority'][0] == \
            'Must be between 1 and 5.'

    def test_add_feature_request_no_client_data(self):
        u"""
        Test adding a new feature request with invalid "client" data.
        """
        test_data = deepcopy(self.test_data)
        del test_data['client']
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['client'][0] == \
            'Missing data for required field.'

    def test_add_feature_request_no_product_area_data(self):
        u"""
        Test adding a new feature request with invalid "product_area" data.
        """
        test_data = deepcopy(self.test_data)
        del test_data['product_area']
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['product_area'][0] == \
            'Missing data for required field.'

    def test_add_feature_request_no_title_data(self):
        u"""
        Test adding a new feature request with no "title" data.
        """
        test_data = deepcopy(self.test_data)
        del test_data['title']
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['title'][0] == \
            'Missing data for required field.'

    def test_add_feature_request_check_client_priority_reordering(self):
        u"""
        Test "client_priority" reordering when a new feature request
        is added with the same "client_priority" value.
        """
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Feature request added'
        first_id, first_client_priority = \
            response_data['data'][0]['id'],\
            response_data['data'][0]['client_priority']

        assert first_id == 1
        assert first_client_priority == 1

        # Sending same client_priority again will result in moving the first
        # priority to 2
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Feature request added'
        second_id, second_client_priority = \
            response_data['data'][0]['id'],\
            response_data['data'][0]['client_priority']

        first_feature_request = FeatureRequest.query.get(first_id)
        assert first_feature_request.id == 1

        # "client_priority" gets reordered when another feature request
        # is added with the same (first) "client_priority" value.
        assert first_feature_request.client_priority == 2
        assert second_id == 2
        assert second_client_priority == 1

    def test_add_feature_request_check_client_priority_no_reordering(
            self):
        u"""
        Test "client_priority" incrementing when a new feature request
        is added.
        """
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Feature request added'
        first_id, first_client_priority = \
            response_data['data'][0]['id'],\
            response_data['data'][0]['client_priority']

        assert first_id == 1
        assert first_client_priority == 1

        test_data = deepcopy(self.test_data)
        test_data['client_priority'] = 2
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Feature request added'
        second_id, second_client_priority = \
            response_data['data'][0]['id'],\
            response_data['data'][0]['client_priority']

        first_feature_request = FeatureRequest.query.get(first_id)

        assert first_feature_request.id == 1

        # "client_priority" gets incremented when another feature request
        # is added.
        assert first_feature_request.client_priority == 1
        assert second_id == 2
        assert second_client_priority == 2

    def test_updating_feature_request_description(self):
        u"""
        Test updating a feature request's description.
        """
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Feature request added'
        description = response_data['data'][0]['description']

        assert description == self.test_data['description']

        # update feature request description
        self.test_data['description'] = "Test feature request\
             updated description"
        response = self.app.post(
            '/api/feature_requests/update/1/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['data'][0]['description'] ==\
            self.test_data['description']

    def test_updating_feature_request_client_priority(self):
        u"""
        Test "client_priority" reordering when a feature request
        is updated.
        """
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Feature request added'
        client_priority = response_data['data'][0]['client_priority']

        assert client_priority == self.test_data['client_priority']

        # update feature request "client_priority" value
        self.test_data['client_priority'] = 2
        response = self.app.post(
            '/api/feature_requests/update/1/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['data'][0]['client_priority'] ==\
            self.test_data['client_priority']

    def test_updating_feature_requests_client_priority(self):
        u"""
        Test "client_priority" reordering when a feature request
        is updated (skipped values; priority from 1 & 2 to 1 & 3).
        """
        for turn in range(1, 3):
            self.test_data['client_priority'] = turn
            response = self.app.post(
                '/api/feature_requests/add/',
                data=json.dumps(self.test_data),
                content_type='application/json'
            )
            response_data = json.loads(response.get_data().decode('utf-8'))
            assert response_data['message'] == 'Feature request added'
            client_priority = response_data['data'][0]['client_priority']

        assert client_priority == self.test_data['client_priority']

        # update feature request "client_priority"
        self.test_data['client_priority'] = 3
        response = self.app.post(
            '/api/feature_requests/update/2/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['data'][0]['client_priority'] ==\
            self.test_data['client_priority']
        assert FeatureRequest.query.get(1).client_priority == 1
        assert FeatureRequest.query.get(2).client_priority == 3

    def test_add_feature_request_invalid_target_date(self):
        u"""
        Test adding a feature request with a non-existent
        target_date value (31 Apr 2019).
        """
        test_data = deepcopy(self.test_data)

        # given "target_date" value does not exist (31 Apr 2019)
        test_data['target_date'] = '2019-04-31'
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['target_date'][0] ==\
            'Not a valid date.'

    def test_delete_feature_request(self):
        u"""
        Test deleting a feature request.
        """
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Feature request added'

        response = self.app.delete(
            '/api/feature_requests/delete/1/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Feature request deleted'

    def test_delete_feature_request_without_id(self):
        u"""
        Test deleting a feature request with an
        incorrect ID.
        """
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Feature request added'

        response = self.app.delete(
            '/api/feature_requests/delete/100/',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] ==\
            'Couldn\'t find feature request with given ID!'


if __name__ == '__main__':
    unittest.main()
