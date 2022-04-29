from flask import Blueprint

from comment.extends import cache
from model.tag import Tag
from schema.tag import TagSchema
from utils.response import parameter_handler, pagination_result

tg = Blueprint('tag', __name__, url_prefix='/tag')


@tg.route('/list', methods=['GET'])
@cache.cached(query_string=True)
def _list():
    page, pages, sort = parameter_handler(Tag, '-create_time')
    pagination = Tag.query.paginate(page, per_page=pages, error_out=False)
    return pagination_result(TagSchema(), pagination)
