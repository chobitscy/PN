from flask import Blueprint, jsonify

from comment.extends import cache
from model.follow import Follow
from model.video import Video
from schema.video import VideoSchema
from template.result import format_result
from utils.response import parameter_handler, pagination_result, error, get_from
from wrapper.auth import auth

fl = Blueprint('follow', __name__, url_prefix='/follow')


# 查询关注列表
def _list(uid):
    key = '_follow_by_%d' % uid
    ch = cache.get(key)
    if ch is None:
        result = Follow.query.filter(Follow.uid == uid).all()
        cache.set(key, result, timeout=60 * 60 * 1)
        return result
    return ch


@fl.route('/page', methods=['GET'])
@auth
def _page(uid):
    pid_list = [n.pid for n in _list(uid)]
    if len(pid_list) == 0:
        return jsonify(format_result([], 1, 0, 0))
    page, pages, sort = parameter_handler(Video, '-creat_date')
    pagination = Video.query.filter(Video.pid.in_(pid_list)).order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)
