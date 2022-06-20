from flask import Blueprint

from comment.extends import cache, db
from model.collection import Collection
from schema.collection import CollectionSchema
from template.result import operation_response, data_response
from utils.response import parameter_handler, error, pagination_result, get_from
from wrapper.auth import auth

cl = Blueprint('collection', __name__, url_prefix='/collection')


@cl.route('/page', methods=["GET"])
@cache.cached(query_string=True)
def _page():
    page, pages, sort = parameter_handler(Collection, "-create_time")
    pagination = Collection.query \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(CollectionSchema(), pagination)


@cl.route("/list/<uid>", methods=["GET"])
def _list(uid: str):
    data = Collection.query.filter(Collection.uid == uid)
    return data_response(data)


@cl.route("/add", methods=["POST"])
@auth
def _add(uid):
    title = get_from("title", str)
    describe = get_from("describe", str)
    record = Collection(uid, title, describe)
    db.session.add(record)
    db.session.commit()
    return operation_response(True)


@cl.route("/remove", methods=["DELETE"])
@auth
def _del(uid):
    _id = get_from("id", str)
    record = Collection.query.filter(Collection.id == _id, Collection.uid == uid).first()
    if record is None:
        error("list not find", 500)
    db.session.remove(record)
    db.session.commit()
    return operation_response(True)


@cl.route("/update", methods=["POST"])
@auth
def _update(uid):
    title = get_from("title", str)
    describe = get_from("describe", str)
    cover = get_from("cover", str)
    Collection.query.filter(Collection.id == uid).update({"title": title, "describe": describe, "cover": cover})
    db.session.commit()
    return operation_response(True)
