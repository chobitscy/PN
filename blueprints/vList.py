from flask import Blueprint

from comment.extends import cache, db
from model.vList import VList
from schema.vList import VListSchema
from template.result import operation_response, data_response
from utils.response import parameter_handler, error, pagination_result, get_from
from wrapper.auth import auth

vl = Blueprint('vList', __name__, url_prefix='/vList')


@vl.route('/page', methods=["GET"])
@cache.cache(query_string=True)
def _page():
    page, pages, sort = parameter_handler(VList, "-create_time")
    pagination = VList.query \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VListSchema(), pagination)


@vl.route("/list/<uid>", methods=["GET"])
def _list(uid: str):
    data = VList.query.filter(VList.uid == uid)
    return data_response(data)


@vl.route("/add", methods=["POST"])
@auth
def _add(uid):
    title = get_from("title", str)
    describe = get_from("describe", str)
    record = VList(uid, title, describe)
    db.session.add(record)
    db.session.commit()
    return operation_response(True)


@vl.route("/remove", methods=["DELETE"])
@auth
def _del(uid):
    _id = get_from("id", str)
    record = VList.query.filter(VList.id == _id, VList.uid == uid).first()
    if record is None:
        error("list not find", 500)
    db.session.remove(record)
    db.session.commit()
    return operation_response(True)


@vl.route("/update", methods=["POST"])
@auth
def _update(uid):
    title = get_from("title", str)
    describe = get_from("describe", str)
    cover = get_from("cover", str)
    VList.query.filter(VList.id == uid).update({"title": title, "describe": describe, "cover": cover})
    db.session.commit()
    return operation_response(True)
