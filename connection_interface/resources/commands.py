from models import Object, ObjectSchema
import requests
from flask import abort
from config import db


def send_command(id, new_value):
    obj = Object.query \
        .filter_by(id=id) \
        .first()

    object_schema = ObjectSchema(many=False)

    st = object_schema.dump(obj).data

    ## convert consumption type dictionary
    combined_object_schema = dict()
    combined_object_schema.update(st)  # add the object to the list

    link = 'http://remote:SelficientUSP@192.168.8.5/scada-remote?m=json&r=grp&fn=write&alias={}&value={}' \
        .format(st['address'], new_value)

    if(st['id'] >= 9):
        abort(405)

    r = requests.get(url=link)
    if(r.status_code == 200):
        combined_object_schema["current_value"] = new_value

    return combined_object_schema
