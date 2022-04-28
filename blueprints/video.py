import datetime
from flask import Blueprint

from comment.cache import cache
from model.video import Video
from schema.video import VideoSchema
from utils.response import parameter_handler, error, pagination_result, search, condition_way

vd = Blueprint('video', __name__)


# 流行
@vd.route('/popular/<type_id>/<day>', methods=['GET'])
@cache.cached(query_string=True)
def popular(type_id, day):
    page, pages, sort = parameter_handler(Video, '-rate')
    try:
        day = int(day)
        type_id = int(type_id)
    except ValueError:
        error('parameter error', 400)
    now = datetime.datetime.now()
    pagination = Video.query \
        .filter(Video.pub_date.between(now - datetime.timedelta(days=day), now),
                Video.type_id == type_id) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)


# 搜索
@vd.route('/search/<vid>', methods=['GET'])
@cache.cached(query_string=True)
def vid_search(vid: str):
    return search(Video, 'vid', vid, condition_way.LIKE.value)


# 产品
@vd.route('/product/<product>', methods=['GET'])
@cache.cached(query_string=True)
def product_search(product: str):
    return search(Video, 'product', product, condition_way.EQUAL.value)


# 作者
@vd.route('/author/<author>', methods=['GET'])
@cache.cached(query_string=True)
def author_search(author: str):
    return search(Video, 'author', author, condition_way.EQUAL.value)
