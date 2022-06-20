from flask import Blueprint

from comment.extends import db
from model.element import Element
from schema.element import RecordSchema
from template.result import operation_response
from utils.response import parameter_handler, error, pagination_result, get_from

el = Blueprint('element', __name__, url_prefix='/element')


@el.route("/push", methods=["POST"])
def _push():
    vlist_id = get_from("vlist_id", str)
    vid = get_from("vid", str)
    record = Element(vlist_id, vid)
    db.session.add(record)
    db.session.commit()
    return operation_response(True)


@el.route("/pull", methods=["DELETE"])
def _pull():
    _id = get_from("id", str)
    record = Element.query.filter(Element.id == _id).first()
    if record is None:
        error("record is null", 500)
    db.session.remove(record)
    db.session.commit()
    return operation_response(True)


@el.route("/page/<_id>", methods=["GET"])
def _record_page(_id: str):
    page, pages, sort = parameter_handler(Element, "-create_time")
    pagination = Element.query \
        .filter(Element.id == _id) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(RecordSchema(), pagination)
