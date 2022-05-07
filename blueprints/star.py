from flask import Blueprint, request, jsonify

from comment.extends import db
from model.star import Star
from schema.star import StarSchema
from utils.response import parameter_handler, pagination_result, error, get_from
from wrapper.auth import auth

sr = Blueprint('star', __name__, url_prefix='/star')


@sr.route('/list', methods=['GET'])
@auth
def _list(_id):
    page, pages, sort = parameter_handler(Star, '-update_time')
    pagination = Star.query.filter(Star.uid == _id).paginate(page, per_page=pages, error_out=False)
    return pagination_result(StarSchema(), pagination)


@sr.route('/add', methods=['POST'])
@auth
def _add(_id):
    vid = request.form.get('vid') or None
    if vid is None:
        error('vid is required', 400)
    star = Star(vid, _id)
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
