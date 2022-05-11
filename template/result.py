def format_result(record: list, page: int, pages: int, total: int) -> dict:
    """
    分页结果模板
    :param record: 记录
    :param page: 第 n 页
    :param pages: 每页 n 条数据
    :param total: 总数
    :return:
    """
    return {
        'data': {
            'record': record,
            'page': page,
            'pages': pages,
            'total': total
        }
    }
