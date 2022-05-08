from flask import Blueprint, request, jsonify

from comment.extends import db, cache, redis_client
from model.follow import Follow
from model.video import Video
from schema.video import VideoSchema
from utils.response import parameter_handler, pagination_result, error, get_from
from wrapper.auth import auth

fl = Blueprint('follow', __name__, url_prefix='/follow')


# 查询关注列表
def _list(uid):
    key = '_follow_by_%d' % uid
    ch = cache.get(key)
    if ch is None:
        result = Follow.query.filter(Follow.uid == uid).all()
        cache.set(key, result, timeout=60 * 60 * 24)
        return result
    return ch


# 删除缓存
def del_ch(uid):
    key = '_follow_by_%d' % uid
    if cache.get(key) is not None:
        cache.delete(key)


@fl.route('/page', methods=['GET'])
@auth
def _page(uid):
    pid_list = [n.pid for n in _list(uid)]
    page, pages, sort = parameter_handler(Video, '-update_time')
    pagination = Video.query.filter(Video.pid.in_(pid_list)).order_by(sort)\
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)


@fl.route('/add', methods=['POST'])
@auth
def _add(uid):
    pid = request.form.get('pid') or None
    follow = Follow(pid, uid)
    db.session.add(follow)
    db.session.commit()
    del_ch(uid)
    # todo delay update product
    redis_client.lpush('delay_follow', pid)
    return jsonify({
        'message': 'ok'
    })


@fl.route('/remove', methods=['DELETE'])
@auth
def _remove(uid):
    _id = get_from('id')
    follow = Follow.query.filter(Follow.id == _id, Follow.uid == uid).first()
    if follow is None:
        error('follow not exist', 500)
    db.session.delete(follow)
    db.session.commit()
    del_ch(uid)
    return jsonify({
        'message': 'ok'
    })
