from flask import Blueprint

from comment.extends import db
from model.record import Record
from schema.record import RecordSchema
from template.result import operation_response
from utils.response import parameter_handler, error, pagination_result, get_from

rd = Blueprint('record', __name__, url_prefix='/record')


@rd.route("/push", methods=["POST"])
def _push():
    vlist_id = get_from("vlist_id", str)
    vid = get_from("vid", str)
    record = Record(vlist_id, vid)
    db.session.add(record)
    db.session.commit()
    return operation_response(True)


@rd.route("/pull", methods=["DELETE"])
def _pull():
    _id = get_from("id", str)
    record = Record.query.filter(Record.id == _id).first()
    if record is None:
        error("record is null", 500)
    db.session.remove(record)
    db.session.commit()
    return operation_response(True)


@rd.route("/record/page/<_id>", methods=["GET"])
def _record_page(_id: str):
    page, pages, sort = parameter_handler(Record, "-create_time")
    pagination = Record.query \
        .filter(Record.id == _id) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(RecordSchema(), pagination)
