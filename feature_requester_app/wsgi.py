from feature_requester_app import app
from feature_requester_app.config import DebugConfiguration

app.config.from_object(DebugConfiguration)

import feature_requester_app.views
