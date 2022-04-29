from flask import Blueprint

from comment.extends import cache
from model.product import Product
from schema.product import ProductSchema
from utils.response import parameter_handler, pagination_result

pd = Blueprint('product', __name__, url_prefix='/product')


@pd.route('/list', methods=['GET'])
@cache.cached(query_string=True)
def _list():
    page, pages, sort = parameter_handler(Product, '-create_time')
    pagination = Product.query.paginate(page, per_page=pages, error_out=False)
    return pagination_result(ProductSchema(), pagination)
