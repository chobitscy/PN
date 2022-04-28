import json
from enum import Enum

from flask import make_response, abort, jsonify, request

from comment.db import db
from model.video import Video
from schema.base import BaseSchema
from schema.video import VideoSchema


def error(message, code):
    abort(make_response(jsonify({'message': message}), code))


def parameter_handler(o: db.Model, default_sort):
    page = request.args.get('page', 1, int)
    pages = request.args.get('pages', 10, int)
    sort = request.args.get('sort_by', default_sort, str)
    sort_way = sort[0]
    sort_by = sort[1:]
    attribute = None
    if hasattr(o, sort_by):
        attribute = getattr(o, sort_by)
        if sort_way == '-':
            attribute = attribute.desc()
    else:
        error('parameter error', 400)
    return page, pages, attribute


class condition_way(Enum):
    LIKE = 1
    EQUAL = 2


def search(model: object, attribute: str, target: object, way: int):
    if hasattr(model, attribute) is False:
        raise ValueError('attribute error')
    condition = None
    if way == condition_way.LIKE.value:
        condition = getattr(model, attribute).like('%' + str(target) + '%')
    elif way == condition_way.EQUAL.value:
        condition = getattr(model, attribute) == target
    if condition is None:
        raise ValueError('condition error')
    page, pages, sort = parameter_handler(Video, '-rate')
    pagination = model.query \
        .filter(condition) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)


def pagination_result(o: BaseSchema, pagination):
    return jsonify({
        'data': {
            'record': json.loads(o.dumps(pagination.items, many=True)),
            'page': pagination.page,
            'pages': pagination.pages,
            'total': pagination.total
        }
    })
