from datetime import datetime
from collections import defaultdict

from .models import db, FeatureRequest
from marshmallow import ValidationError


def validate_date_in_future(value):
    if value < datetime.now().date():
        raise ValidationError('Target date must be in the future')


def update_client_priorities(new_client_priority):
    all_feature_requests = defaultdict()
    all_feature_requests_db = FeatureRequest.query.all()

    for feature_request in all_feature_requests_db:
        all_feature_requests.setdefault(
            feature_request.client_priority,
            feature_request.id
        )

    if new_client_priority not in all_feature_requests.keys():
        return
    else:
        tmp_client_priority = new_client_priority
        while tmp_client_priority in all_feature_requests.keys():
            tmp_client_priority = tmp_client_priority + 1

        while tmp_client_priority > new_client_priority:
            feature_request_updated = FeatureRequest.query.get(
                all_feature_requests[tmp_client_priority - 1]
            )
            feature_request_updated.client_priority = tmp_client_priority

            db.session.add(feature_request_updated)

            tmp_client_priority = tmp_client_priority - 1

        db.session.commit()
        return
