from models import ConsumptionType, ConsumptionTypeSchema, Object, ObjectSchema
from flask import abort


def send_command(id, consumption_type, new_value):
    obj = Object.query \
        .filter_by(id=id) \
        .first()

    cst_type = ConsumptionType.query \
             .filter_by(name=consumption_type) \
             .first()

    if obj is None or cst_type is None:
        abort(404)

    object_schema = ObjectSchema(many=False)
    cst_schema = ConsumptionTypeSchema(many=False)

    st = object_schema.dump(obj).data

    ## convert consumption type dictionary
    combined_object_schema = dict()
    converted_cst_schema = cst_schema.dump(cst_type).data
    combined_object_schema.update({'consumption_type_id': converted_cst_schema["id"]})
    combined_object_schema.update({'consumption_type': converted_cst_schema["name"]})
    combined_object_schema.update(st) # add the object to the list

    return combined_object_schema
