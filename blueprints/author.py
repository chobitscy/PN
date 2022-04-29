from flask import Blueprint

from comment.extends import cache
from model.author import Author
from schema.author import AuthorSchema
from utils.response import parameter_handler, pagination_result

ah = Blueprint('author', __name__, url_prefix='/author')


@ah.route('/list', methods=['GET'])
@cache.cached(query_string=True)
def _list():
    page, pages, sort = parameter_handler(Author, '-create_time')
    pagination = Author.query.paginate(page, per_page=pages, error_out=False)
    return pagination_result(AuthorSchema(), pagination)
