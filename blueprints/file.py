import os

from flask import Blueprint, request, send_file
from werkzeug.utils import secure_filename

from template.result import operation_response
from utils.response import error, get_from

fe = Blueprint('file', __name__, url_prefix='/file')

path = 'screenshot'

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
if not os.path.exists(path):
    os.makedirs(path)


@fe.route('/update', methods=['POST'])
def _update():
    file = request.files['file']
    name = get_from('name', str)
    file.save(os.path.join(path, secure_filename(name)))
    return operation_response(True)


@fe.route('/download/<filename>', methods=['GET'])
def _download(filename):
    file_path = '%s/%s' % (path, filename)
    if not os.path.exists(file_path):
        error('file not find', 500)
    return send_file(file_path)
