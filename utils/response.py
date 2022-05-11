import json
from enum import Enum

from flask import make_response, abort, jsonify, request

from comment.extends import db
from schema.base import BaseSchema
from template.result import format_result


def error(message, code):
    abort(make_response(jsonify({'message': message}), code))


def parameter_handler(model: db.Model, default_sort):
    """
    请求参数处理
    :param model: model 类
    :param default_sort: 默认排序字段
    :return: 当前页，页数，排序
    """
    page = request.args.get('page', 1, int)
    pages = request.args.get('pages', 10, int)
    sort = request.args.get('sort_by', default_sort, str)
    sort_way = sort[0]
    sort_by = sort[1:]
    attribute = None
    if hasattr(model, sort_by):
        attribute = getattr(model, sort_by)
        if sort_way == '-':
            attribute = attribute.desc()
    else:
        error('parameter error', 400)
    return page, pages, attribute


class condition_way(Enum):
    LIKE = 1
    EQUAL = 2


def search(model: object, attribute: str, target: object, way: int, sort: str, schema: BaseSchema):
    """
    搜索封装方法
    :param model: model 类
    :param attribute: 查询字段
    :param target: 查询参数
    :param way: 查询方法
    :param sort: 排序
    :param schema 序列化对象
    :return: 分页
    """
    if hasattr(model, attribute) is False:
        raise ValueError('attribute error')
    condition = None
    if way == condition_way.LIKE.value:
        condition = getattr(model, attribute).like('%' + str(target) + '%')
    elif way == condition_way.EQUAL.value:
        condition = getattr(model, attribute) == target
    if condition is None:
        raise ValueError('condition error')
    if hasattr(model, sort) is False:
        raise ValueError('sort error')
    page, pages, sort = parameter_handler(model, '-' + sort)
    pagination = model.query \
        .filter(condition) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(schema, pagination)


def pagination_result(schema: BaseSchema, pagination):
    """
    分页结果封装类
    :param schema: 序列化对象
    :param pagination: 分页结果
    :return: json
    """
    return jsonify(
        format_result(
            json.loads(schema.dumps(pagination.items, many=True)),
            pagination.page,
            pagination.pages,
            pagination.total
        )
    )


def get_from(arg):
    value = request.form.get(arg) or None
    if value is None:
        error('%s is required' % arg, 400)
    return value
