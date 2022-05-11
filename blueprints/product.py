from flask import Blueprint, jsonify, request

from comment.extends import cache, db, redis_client
from model.follow import Follow
from model.product import Product
from schema.product import ProductSchema
from utils.response import parameter_handler, pagination_result, search, condition_way, get_from, error
from wrapper.auth import auth

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


@pd.route('/follow', methods=['POST'])
@auth
def _add(uid):
    pid = request.form.get('pid') or None
    follow = Follow(pid, uid)
    db.session.add(follow)
    db.session.commit()
    del_ch(uid)
    # delay update product
    redis_client.lpush('delay_follow', pid)
    return jsonify({
        'message': 'ok'
    })


@pd.route('/unfollow', methods=['DELETE'])
@auth
def _remove(uid):
    _id = get_from('id')
    follow = Follow.query.filter(Follow.id == _id, Follow.uid == uid).first()
    if follow is None:
        error('follow not exist', 500)
    db.session.delete(follow)
    db.session.commit()
    del_ch(uid)
    redis_client.lrem('delay_follow', 1, follow.pid)
    return jsonify({
        'message': 'ok'
    })


# 删除缓存
def del_ch(uid):
    key = '_follow_by_%d' % uid
    if cache.get(key) is not None:
        cache.delete(key)
