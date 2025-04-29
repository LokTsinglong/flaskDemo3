from flask import Blueprint


workspace_main = Blueprint('workspace_main', __name__)

#延迟导入，否则可能会有(most likely due to a circular import
from .workspace1 import workspace1_api
workspace_main.register_blueprint(workspace1_api, url_prefix='/workspace1')