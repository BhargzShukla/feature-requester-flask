from datetime import datetime

from flask import jsonify, render_template, request, send_from_directory
from sqlalchemy.orm.exc import UnmappedInstanceError

from feature_requester_app import app

from .models import Client, FeatureRequest, ProductArea, db
from .schema import ClientSchema, FeatureRequestSchema, ProductAreaSchema
from .util import update_client_priorities


def _build_feature_request(feature_request, data):
    u"""
    Private method to build a feature request object.
    """
    for field in [
        'title',
        'description',
        'client_id',
        'client_priority',
        'product_area_id',
        'target_date'
    ]:
        setattr(
            feature_request,
            field,
            data.get(
                field,
                getattr(feature_request, field)
            )
        )

    return feature_request


@app.route('/favicon.ico')
def get_favicon():
    return send_from_directory('static', 'favicon.ico')


@app.route('/')
def home_page():
    u"""
    Render the app's home page.
    """
    return render_template('home.html')


@app.route('/api/clients/', methods=['GET'])
def get_all_clients():
    u"""
    GET a JSON response of all clients from database.
    """
    clients = Client.query.all()
    client_schema = ClientSchema()
    clients_json = client_schema.dump(clients, many=True)
    return jsonify({'clients': clients_json.data})


@app.route('/api/product_areas/', methods=['GET'])
def get_all_product_areas():
    u"""
    GET a JSON response of all product areas from database.
    """
    product_areas = ProductArea.query.all()
    product_area_schema = ProductAreaSchema()
    product_areas_json = product_area_schema.dump(product_areas, many=True)
    return jsonify({'product_areas': product_areas_json.data})


@app.route('/api/feature_requests/', methods=['GET'])
def get_all_feature_requests():
    u"""
    GET a JSON response of all feature requests from database.
    """
    feature_requests = FeatureRequest.query.all()
    feature_request_schema = FeatureRequestSchema()
    feature_requests_json = feature_request_schema.dump(
        feature_requests,
        many=True
    )
    return jsonify({'feature_requests': feature_requests_json.data})


@app.route('/api/feature_requests/update/<int:id>/', methods=['POST'])
def update_feature_request(id=None):
    u"""
    API method to update data in an existing feature request.
    
    # TODO: Implement a front-end for updating requests.
    """
    if not id:
        return jsonify(
            {
                'message': 'ID required to update request!'
            }
        ), 400
    json_response_data = request.get_json()
    feature_request = FeatureRequest.query.get(id)

    if not feature_request:
        return jsonify(
            {
                'message': 'Couldn\'t find feature request with given ID!'
            }
        ), 400

    try:
        if feature_request.target_date != datetime.strptime(
            json_response_data['target_date'], '%Y-%m-%d'
        ).date():
            feature_request_schema = FeatureRequestSchema()
        else:
            feature_request_schema = FeatureRequestSchema(
                exclude=['target-date']
            )
    except ValueError as error:
        return jsonify(
            {
                'errors': {
                    'target_date': str(error)
                }
            }
        ), 422

    data, errors = feature_request_schema.load(json_response_data)
    if errors:
        return jsonify(
            {
                'errors': errors
            }
        ), 422

    update_client_priorities(data['client_priority'])
    feature_request = _build_feature_request(feature_request, data)

    db.session.add(feature_request)
    db.session.commit()

    return jsonify(
        {
            'message': 'Feature request updated',
            'data': FeatureRequestSchema().dump(feature_request)
        }
    ), 200


@app.route('/api/feature_requests/delete/<int:id>/', methods=['DELETE'])
def delete_feature_request(id=None):
    u"""
    API method to delete a feature request from database.
    
    # TODO: Implement a front-end to delete requests.
    """
    if not id:
        return jsonify(
            {
                'message': 'ID required to delete request!'
            }
        ), 400
    feature_request = FeatureRequest.query.get(id)

    if not feature_request:
        return jsonify(
            {
                'message': 'Couldn\'t find feature request with given ID!'
            }
        ), 400

    try:
        db.session.delete(feature_request)
        db.session.commit()
    except UnmappedInstanceError:
        return jsonify(
            {
                'message': 'Couldn\'t delete feature request!'
            }
        ), 422

    return jsonify(
        {
            'message': "Feature request deleted"
        }
    ), 200


@app.route('/api/feature_requests/add/', methods=['POST'])
def add_new_feature_request():
    u"""
    API method to add a new feature request to database.
    """
    feature_request_schema = FeatureRequestSchema()
    json_response_data = request.get_json()

    if not json_response_data:
        return jsonify(
            {
                'message': 'No input provided'
            }
        ), 400

    data, errors = feature_request_schema.load(json_response_data)

    if errors:
        return jsonify(
            {
                'errors': errors
            }
        ), 400

    update_client_priorities(data['client_priority'])
    feature_request = FeatureRequest()
    feature_request = _build_feature_request(feature_request, data)

    db.session.add(feature_request)
    db.session.commit()

    return jsonify(
        {
            'message': 'Feature request added',
            'data': FeatureRequestSchema().dump(feature_request)
        }
    ), 201
