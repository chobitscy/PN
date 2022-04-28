from flask import Blueprint

from comment.cache import cache
from model.star import Star
from schema.star import StarSchema
from utils.response import parameter_handler, pagination_result

sr = Blueprint('star', __name__, url_prefix='/star')


@sr.route('/list', methods=['GET'])
@cache.cached(query_string=True)
def _list():
    page, pages, sort = parameter_handler(Star, '-update_time')
    pagination = Star.query.paginate(page, per_page=pages, error_out=False)
    return pagination_result(StarSchema(), pagination)
