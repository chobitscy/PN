import datetime
import json

from flask import Blueprint

from comment.cache import cache
from model.author import Author
from model.product import Product
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


@vd.route('/test', methods=['GET'])
def test():
    page, pages, sort = parameter_handler(Video, '-rate')
    pagination = Video.query \
        .join(Product, Video.product == Product.id) \
        .join(Author, Video.author == Author.id) \
        .order_by(sort) \
        .with_entities(Video, Product.name, Author.name) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)


@vd.route('/search/<vid>', methods=['GET'])
@cache.cached(query_string=True)
def vid_search(vid: str):
    return search(Video, 'vid', vid, condition_way.EQUAL.value)


@vd.route('/product/<pid>', methods=['GET'])
@cache.cached(query_string=True)
def product_search(pid: int):
    return search(Video, 'product', pid, condition_way.EQUAL.value)


@vd.route('/author/<aid>', methods=['GET'])
@cache.cached(query_string=True)
def author_search(aid: int):
    return search(Video, 'author', aid, condition_way.EQUAL.value)
