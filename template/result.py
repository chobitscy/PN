from flask import jsonify


def pagination_response(record: list, page: int, pages: int, total: int) -> jsonify:
    """
    分页结果模板
    :param record: 记录
    :param page: 第 n 页
    :param pages: 每页 n 条数据
    :param total: 总数
    :return:
    """
    return jsonify({
        'code': 1,
        'message': 'ok',
        'data': {
            'record': record,
            'page': page,
            'pages': pages,
            'total': total
        }
    })


def operation_response(success: bool) -> jsonify:
    """
    增删改结果模板
    :param success: 是否成功
    :return:
    """
    return jsonify({
        'code': 1 if success else 0,
        'message': 'ok' if success else 'error'
    })


def data_response(data) -> jsonify:
    """
    数据果模板
    :param data: 数据
    :return:
    """
    return jsonify({
        'code': 1,
        'message': 'ok',
        'data': data
    })
