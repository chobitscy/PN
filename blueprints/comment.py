import datetime
import json

from flask import Blueprint, request, jsonify

from model.comment import Comment
from model.user import User
from schema.comment import CommentSchema
from template.result import format_result
from wrapper.auth import auth

cm = Blueprint('comment', __name__, url_prefix='/comment')


@cm.route('/push', methods=['POST'])
@auth
def _push(uid):
    vid = request.form.get('vid', type=int)
    content = request.form.get('content', type=str)
    username = User.query.filter(User.id == uid).first().email
    Comment(uid=uid, vid=vid, username=username, content=content, create_time=datetime.datetime.now()).save()
    return 'ok'


@cm.route('/page/<vid>', methods=['GET'])
def _page(vid: int):
    page = request.args.get('page', 1, int)
    pages = request.args.get('pages', 10, int)
    result = Comment.objects(vid=vid).paginate(page=page, per_page=pages)
    return jsonify(
        format_result(
            json.loads(CommentSchema().dumps(result.items, many=True)),
            result.page,
            result.pages,
            result.total
        )
    )
