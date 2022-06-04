import datetime

from flask import Blueprint, jsonify

from comment.extends import cache, db
from model.video import Video
from schema.video import VideoSchema
from template.result import operation_response
from utils.response import parameter_handler, error, pagination_result, search, condition_way, get_from

vd = Blueprint('video', __name__, url_prefix='/video')


@vd.route('/popular/<day>', methods=['GET'])
@cache.cached(query_string=True)
def popular(day):
    page, pages, sort = parameter_handler(Video, '-rate')
    try:
        day = int(day)
    except ValueError:
        error('parameter error', 400)
    now = datetime.datetime.now()
    pagination = Video.query \
        .filter(Video.pub_date.between(now - datetime.timedelta(days=day), now), Video.create_date is not None) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)


@vd.route('/page', methods=['GET'])
@cache.cached(query_string=True)
def _list():
    page, pages, sort = parameter_handler(Video, '-create_time')
    pagination = Video.query \
        .filter(Video.create_date is not None) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)


@vd.route('/search/<vid>', methods=['GET'])
@cache.cached(query_string=True)
def _search(vid: str):
    return search(Video, 'vid', vid, condition_way.EQUAL.value, 'rate', VideoSchema())


@vd.route('/detail/<_id>', methods=['GET'])
@cache.cached(query_string=True)
def _detail(_id: int):
    detail = Video.query.filter(Video.id == _id).first()
    return jsonify({
        'data': VideoSchema().dump(detail)
    })


@vd.route('/product/<pid>', methods=['GET'])
@cache.cached(query_string=True)
def _pd(pid: int):
    page, pages, sort = parameter_handler(Video, '-rate')
    pagination = Video.query.filter(Video.pid == pid).order_by(sort).paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)


@vd.route('/mark', methods=['POST'])
def _mark():
    _id = get_from('id', str)
    Video.query.filter(Video.id == _id).update({'uncensored': 0})
    db.session.commit()
    video = Video.query.filter(Video.id == _id).first()
    Video.query.filter(Video.pid == video.pid).update({'uncensored': 0})
    db.session.commit()
    return operation_response(True)


@vd.route('/unmark', methods=['POST'])
def _unmark():
    _id = get_from('id', str)
    Video.query.filter(Video.id == _id).update({'uncensored': 1})
    db.session.commit()
    return operation_response(True)
