from models import Object, ConsumptionType, ObjectSchema, ConsumptionTypeSchema
from flask import abort


def get_all():
    """Get all objects
    """
    obj = Object.query \
        .order_by(Object.id) \
        .all()

    if obj is None:
        abort(404)
    object_schema = ObjectSchema(many=True)

    st = object_schema.dump(obj).data
    return st


def get_by_name(name):
    """Get objects by name
    
    Arguments:
        name {string} -- Name of the object
    """
    obj = Object.query \
        .filter_by(name=name) \
        .first()

    if obj is None:
        abort(404)

    object_schema = ObjectSchema(many=False)

    st = object_schema.dump(obj).data
    return st


def get_by_id(id):
    """Get objects by id
    
    Arguments:
        id {int} -- ID of the object
    """
    obj = Object.query.filter_by(id=id).first()

    if obj is None:
        abort(404)

    object_schema = ObjectSchema(many=False)

    st = object_schema.dump(obj).data
    return st
