from flask import Blueprint

from model.follow import Follow
from model.video import Video
from schema.video import VideoSchema
from template.result import pagination_response
from utils.response import parameter_handler, pagination_result
from wrapper.auth import auth

fl = Blueprint('follow', __name__, url_prefix='/follow')


# 查询关注列表
def _list(uid):
    return Follow.query.filter(Follow.uid == uid).all()


@fl.route('/page', methods=['GET'])
@auth
def _page(uid):
    pid_list = [n.pid for n in _list(uid)]
    if len(pid_list) == 0:
        return pagination_response([], 1, 0, 0)
    page, pages, sort = parameter_handler(Video, '-creat_date')
    pagination = Video.query.filter(Video.pid.in_(pid_list)).order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)
