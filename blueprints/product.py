from flask import Blueprint, jsonify

from comment.extends import cache
from model.product import Product
from schema.product import ProductSchema
from utils.response import parameter_handler, pagination_result, search, condition_way

pd = Blueprint('product', __name__, url_prefix='/product')


@pd.route('/page', methods=['GET'])
@cache.cached(query_string=True)
def _page():
    page, pages, sort = parameter_handler(Product, '-create_time')
    pagination = Product.query.order_by(sort).paginate(page, per_page=pages, error_out=False)
    return pagination_result(ProductSchema(), pagination)


@pd.route('/detail/<_id>', methods=['GET'])
@cache.cached(query_string=True)
def _detail(_id: int):
    detail = Product.query.filter(Product.id == _id).first()
    return jsonify({
        'data': ProductSchema().dump(detail)
    })


@pd.route('/search/<name>', methods=['GET'])
@cache.cached(query_string=True)
def _search(name: str):
    return search(Product, 'name', name, condition_way.LIKE.value, 'fans', ProductSchema())
