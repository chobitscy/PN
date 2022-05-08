from flask import Blueprint, request, jsonify

from comment.extends import db
from model.star import Star
from schema.star import StarSchema
from utils.response import parameter_handler, pagination_result, error, get_from
from wrapper.auth import auth

sr = Blueprint('star', __name__, url_prefix='/star')


@sr.route('/page', methods=['GET'])
@auth
def _page(uid):
    page, pages, sort = parameter_handler(Star, '-update_time')
    pagination = Star.query.filter(Star.uid == uid).order_by(sort).paginate(page, per_page=pages, error_out=False)
    return pagination_result(StarSchema(), pagination)


@sr.route('/add', methods=['POST'])
@auth
def _add(uid):
    vid = get_from('vid')
    star = Star(vid, uid)
    db.session.add(star)
    db.session.commit()
    return jsonify({
        'message': 'ok'
    })


@sr.route('/remove', methods=['DELETE'])
@auth
def _remove(uid):
    _id = get_from('id')
    star = Star.query.filter(Star.id == _id, Star.uid == uid).first()
    if star is None:
        error('star not exist', 500)
    db.session.delete(star)
    db.session.commit()
    return jsonify({
        'message': 'ok'
    })
