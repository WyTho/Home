from models import Object, ObjectSchema
import requests
from flask import abort
from config import USE_SIMULATION, SIM_CONTROLLER


def send_command(id, new_value):
    """Handle command send by API
    
    Arguments:
        id {[int]} -- Unique identifier of device
        new_value {[any]} -- The right data for the device
    """
    obj = Object.query \
        .filter_by(id=id) \
        .first()

    object_schema = ObjectSchema(many=False)

    st = object_schema.dump(obj).data

    ## convert consumption type dictionary
    combined_object_schema = dict()
    combined_object_schema.update(st)  # add the object to the list

    if USE_SIMULATION:
        SIM_CONTROLLER.handle_interact(obj.address, new_value)
        combined_object_schema["current_value"] = new_value
    else:
        link = 'http://remote:SelficientUSP@192.168.8.5/scada-remote?m=json&r=grp&fn=write&alias={}&value={}' \
            .format(st['address'], new_value)

        r = requests.get(url=link)
        if (r.status_code == 200):
            combined_object_schema["current_value"] = new_value

    return combined_object_schema
