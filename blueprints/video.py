import datetime

from flask import Blueprint, jsonify

from comment.extends import cache
from model.video import Video
from schema.video import VideoSchema
from utils.response import parameter_handler, error, pagination_result, search, condition_way

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
        .filter(Video.pub_date.between(now - datetime.timedelta(days=day), now)) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)


@vd.route('/page', methods=['GET'])
@cache.cached(query_string=True)
def _list():
    page, pages, sort = parameter_handler(Video, '-create_time')
    pagination = Video.query \
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


@vd.route('/author/<aid>', methods=['GET'])
@cache.cached(query_string=True)
def _ah(aid: int):
    page, pages, sort = parameter_handler(Video, '-rate')
    pagination = Video.query.filter(Video.aid == aid).order_by(sort).paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)