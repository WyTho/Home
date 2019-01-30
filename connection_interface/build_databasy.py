import os
from config import db
from models import Object, ConsumptionType, DataType, Script
import requests
import json

DATATYPES = [
    "1 byte signed integer",  # 1
    "1-bit(boolean)",  # 2
    "1 byte unsigned integer",  # 3
    "1-byte ASCII-character",  # 4
    "2 byte floating point",  # 5
    "2 byte signed integer",  # 6
    "2 byte unsigned integer",  # 7
    "2-bits(1 evaluated bit)",  # 8
    "3 byte date",  # 9
    "3 byte time/day",  # 10
    "3 byte unsigned integer",  # 11
    "4 byte accesscontrol",  # 12
    "4 byte floating point",  # 13
    "4 byte signed integer",  # 14
    "4 byte unsigned integer",  # 15
    "4-bits(3 evaluated bits)",  # 16
    "8 byte signed integer",  # 17
    "14 byte ASCII",  # 18
    "250 byte data"  # 19
]

CONSUMPTIONTYPES = [
    {'name': 'toggle', 'data_type_id': 2},  # 1
    {'name': '1-bit', 'data_type_id': 1},  # 2
    {'name': 'ASCII', 'data_type_id': 4},  # 3
    {'name': '232.600 RGB Color', 'data_type_id': 10},  # 4
]

SCRIPTS = [
    {'name': 'Lamp'},  # 1
    {'name': 'Temperature_target'},  # 2
    {'name': 'Livingroom Temperature'},  # 3
    {'name': 'Heating/Cooling'}  # 4
]

OBJECTS = [
    {'name': 'Badkamer spots', 'address': '0/0/1', 'data_type_id': 2, 'current_value': None, 'script_id': 1},
    {'name': 'Gang lamp', 'address': '0/0/2', 'data_type_id': 2, 'current_value': None, 'script_id': 1},
    {'name': 'Bed left', 'address': '0/0/3', 'data_type_id': 2, 'current_value': None, 'script_id': 1},
    {'name': 'Bed right', 'address': '0/0/4', 'data_type_id': 2, 'current_value': None, 'script_id': 1},
    {'name': 'Plafonier slaap', 'address': '0/0/5', 'data_type_id': 2, 'current_value': None, 'script_id': 1},
    {'name': 'Plafoniere woon', 'address': '0/0/6', 'data_type_id': 2, 'current_value': None, 'script_id': 1},
    {'name': 'lamp corner', 'address': '0/0/7', 'data_type_id': 2, 'current_value': None, 'script_id': 1},
    {'name': 'dining table', 'address': '0/0/8', 'data_type_id': 2, 'current_value': None, 'script_id': 1},
    {'name': 'spots kitchen', 'address': '0/0/9', 'data_type_id': 2, 'current_value': None, 'script_id': 1},

    # RESEARCHDATA
    # Feedback lights

    {'name': 'Badkamer spots FB', 'address': '0/1/1', 'data_type_id': 2, 'current_value': None},
    {'name': 'Gang lamp FB', 'address': '0/1/2', 'data_type_id': 2, 'current_value': None},
    {'name': 'Bed left FB', 'address': '0/1/3', 'data_type_id': 2, 'current_value': None},
    {'name': 'Bed right FB', 'address': '0/1/4', 'data_type_id': 2, 'current_value': None},
    {'name': 'Plafonier slaap FB', 'address': '0/1/5', 'data_type_id': 2, 'current_value': None},
    {'name': 'Plafoniere woon FB', 'address': '0/1/6', 'data_type_id': 2, 'current_value': None},
    {'name': 'lamp corner FB', 'address': '0/1/7', 'data_type_id': 2, 'current_value': None},
    {'name': 'dining table FB', 'address': '0/1/8', 'data_type_id': 2, 'current_value': None},
    {'name': 'spots kitchen FB', 'address': '0/1/9', 'data_type_id': 2, 'current_value': None},

    {'name': 'Badkamer spots VALUE FB', 'address': '0/4/1', 'data_type_id': 3, 'current_value': None},
    {'name': 'Gang lamp VALUE FB', 'address': '0/4/2', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bed left VALUE FB', 'address': '0/4/3', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bed right VALUE FB', 'address': '0/4/4', 'data_type_id': 3, 'current_value': None},
    {'name': 'Plafonier slaap VALUE FB', 'address': '0/4/5', 'data_type_id': 3, 'current_value': None},
    {'name': 'Plafoniere woon VALUE FB', 'address': '0/4/6', 'data_type_id': 3, 'current_value': None},
    {'name': 'lamp corner VALUE FB', 'address': '0/4/7', 'data_type_id': 3, 'current_value': None},
    {'name': 'dining table VALUE FB', 'address': '0/4/8', 'data_type_id': 3, 'current_value': None},
    {'name': 'spots kitchen VALUE FB', 'address': '0/4/9', 'data_type_id': 3, 'current_value': None},

    # RESEARCHDATA
    # Master/slave heating/cooling

    {'name': 'master/slave heating/cooling', 'address': '1/2/0', 'data_type_id': 1, 'current_value': False, 'script_id': 4},
    {'name': 'temperature target', 'address': '1/2/1', 'data_type_id': 5, 'current_value': 20.00, 'script_id': 2},

    # RESEARCHDATA
    # Ventilation

    {'name': 'Bedroom CO2', 'address': '2/0/0', 'data_type_id': 5, 'current_value': None},
    {'name': 'Livingroom CO2', 'address': '2/0/3', 'data_type_id': 5, 'current_value': None},
    {'name': 'Bathroom CO2', 'address': '2/0/6', 'data_type_id': 5, 'current_value': None},

    {'name': 'Bedroom Humidity', 'address': '2/0/1', 'data_type_id': 3, 'current_value': None},
    {'name': 'Livingroom Humidity', 'address': '2/0/4', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bathroom Humidity', 'address': '2/0/7', 'data_type_id': 3, 'current_value': None},

    {'name': 'Bedroom Temperature', 'address': '2/0/2', 'data_type_id': 5, 'current_value': None},
    {'name': 'Livingroom Temperature', 'address': '2/0/5', 'data_type_id': 5, 'current_value': 3.0, 'script_id': 3},
    {'name': 'Bathroom Temperature', 'address': '2/0/8', 'data_type_id': 5, 'current_value': None},

    # RESEARCHDATA
    # Blinds

    {'name': 'Bedroom (manual) Status Height', 'address': '3/4/0', 'data_type_id': 3, 'current_value': None},
    {'name': 'Living  (manual) Status Height', 'address': '3/4/2', 'data_type_id': 3, 'current_value': None},
    {'name': 'Kitchen (manual) Status Height', 'address': '3/4/4', 'data_type_id': 3, 'current_value': None},

    {'name': 'Wind', 'address': '3/5/0', 'data_type_id': 3, 'current_value': None},
    {'name': 'Rain', 'address': '3/5/1', 'data_type_id': 3, 'current_value': None},
    {'name': 'Frost', 'address': '3/5/2', 'data_type_id': 3, 'current_value': None},
    {'name': 'Sensor Alarm', 'address': '3/5/3', 'data_type_id': 3, 'current_value': None},
    {'name': 'Automatic', 'address': '3/5/4', 'data_type_id': 3, 'current_value': None},
    {'name': 'Screen block', 'address': '3/5/5', 'data_type_id': 3, 'current_value': None},

    # RESEARCHDATA
    # Dummy actor Absolute led dimming + feedback

    {'name': 'Livingroom 1 Dim RGBW FB', 'address': '5/6/0', 'data_type_id': 3, 'current_value': None},
    {'name': 'Livingroom 2 Dim RGBW FB', 'address': '5/6/1', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bedroom 1    Dim RGBW FB', 'address': '5/6/2', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bedroom 2    Dim RGBW FB', 'address': '5/6/3', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bathroom     Dim RGBW FB', 'address': '5/6/4', 'data_type_id': 3, 'current_value': None},

    {'name': 'Livingroom 1 Dim R FB', 'address': '5/6/5', 'data_type_id': 3, 'current_value': None},
    {'name': 'Livingroom 2 Dim R FB', 'address': '5/6/6', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bedroom 1    Dim R FB', 'address': '5/6/7', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bedroom 2    Dim R FB', 'address': '5/6/8', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bathroom     Dim R FB', 'address': '5/6/9', 'data_type_id': 3, 'current_value': None},

    {'name': 'Livingroom 1 Dim G FB', 'address': '5/6/10', 'data_type_id': 3, 'current_value': None},
    {'name': 'Livingroom 2 Dim G FB', 'address': '5/6/11', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bedroom 1    Dim G FB', 'address': '5/6/12', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bedroom 2    Dim G FB', 'address': '5/6/13', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bathroom     Dim G FB', 'address': '5/6/14', 'data_type_id': 3, 'current_value': None},

    {'name': 'Livingroom 1 Dim B FB', 'address': '5/6/15', 'data_type_id': 3, 'current_value': None},
    {'name': 'Livingroom 2 Dim B FB', 'address': '5/6/16', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bedroom 1    Dim B FB', 'address': '5/6/17', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bedroom 2    Dim B FB', 'address': '5/6/18', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bathroom     Dim B FB', 'address': '5/6/19', 'data_type_id': 3, 'current_value': None},

    {'name': 'Livingroom 1 Dim W FB', 'address': '5/6/20', 'data_type_id': 3, 'current_value': None},
    {'name': 'Livingroom 2 Dim W FB', 'address': '5/6/21', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bedroom 1    Dim W FB', 'address': '5/6/22', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bedroom 2    Dim W FB', 'address': '5/6/23', 'data_type_id': 3, 'current_value': None},
    {'name': 'Bathroom     Dim W FB', 'address': '5/6/24', 'data_type_id': 3, 'current_value': None},

    # RESEARCHDATA
    # Dummy actor 12 fold actor

    {'name': 'ELAN Mode', 'address': '2/1/1', 'data_type_id': 3, 'current_value': None},
    {'name': 'ELAN pos 1 (FB)', 'address': '5/2/1', 'data_type_id': 2, 'current_value': None},
    {'name': 'ELAN pos 2 (FB)', 'address': '5/2/3', 'data_type_id': 2, 'current_value': None},
    {'name': 'ELAN pos 3 (FB)', 'address': '5/2/5', 'data_type_id': 2, 'current_value': None},
    {'name': 'Lamp TR FB', 'address': '5/2/7', 'data_type_id': 2, 'current_value': None},
    {'name': 'Elan pos 4 (FB)', 'address': '5/2/9', 'data_type_id': 2, 'current_value': None},
    {'name': 'EM Cooling (FB)', 'address': '5/2/11', 'data_type_id': 2, 'current_value': None},
    {'name': 'EM Heating (FB)', 'address': '5/2/13', 'data_type_id': 2, 'current_value': None},
    {'name': 'EM Pomp ELAN (FB)', 'address': '5/2/15', 'data_type_id': 2, 'current_value': None},
    {'name': 'EM Elan pomp V.V.', 'address': '5/2/17', 'data_type_id': 2, 'current_value': None},

    # RESEARCHDATA
    # Dummy Heating actor

    {'name': 'Zone 1 Ouput valve FB', 'address': '5/3/0', 'data_type_id': 3, 'current_value': None},
    {'name': 'Zone 2 Ouput valve FB', 'address': '5/3/1', 'data_type_id': 3, 'current_value': None},
    {'name': 'Zone 3 Ouput valve FB', 'address': '5/3/2', 'data_type_id': 3, 'current_value': None},
    {'name': 'Command value zone 1', 'address': '5/3/3', 'data_type_id': 3, 'current_value': None},
    {'name': 'Command value zone 2', 'address': '5/3/7', 'data_type_id': 3, 'current_value': None},
    {'name': 'Command value zone 3', 'address': '5/3/8', 'data_type_id': 3, 'current_value': None},

    # RESEARCHDATA
    # Presence

    {'name': 'Hallway presence', 'address': '6/1/0', 'data_type_id': 2, 'current_value': None},
    {'name': 'Presence detection alarm', 'address': '6/1/1', 'data_type_id': 2, 'current_value': None},

    # RESEARCHDATA
    # Temperature outdoor

    {'name': 'Brightness', 'address': '6/3/0', 'data_type_id': 2, 'current_value': None},
    {'name': 'Temperature', 'address': '6/3/1', 'data_type_id': 2, 'current_value': None},

    # RESEARCHDATA
    # Scenes

    {'name': 'Alles aan/uit', 'address': '7/4/0', 'data_type_id': 2, 'current_value': None},

    # RESEARCHDATA
    # Combi Sensor

    {'name': 'Twilight measured', 'address': '6/0/0', 'data_type_id': 5, 'current_value': None},
    {'name': 'Wind measured', 'address': '6/0/1', 'data_type_id': 5, 'current_value': None},
    {'name': 'Rain Yes/NO', 'address': '6/0/2', 'data_type_id': 3, 'current_value': None},
    {'name': 'sun east', 'address': '6/0/3', 'data_type_id': 2, 'current_value': None},
    {'name': 'sun south', 'address': '6/0/4', 'data_type_id': 5, 'current_value': None},
    {'name': 'sun west', 'address': '6/0/5', 'data_type_id': 5, 'current_value': None},

    # RESEARCHDATA
    # Doors

    {'name': 'Entrance door open', 'address': '6/4/0', 'data_type_id': 2, 'current_value': None},
    {'name': 'Livingroom door 1a open', 'address': '6/4/1', 'data_type_id': 2, 'current_value': None},
    {'name': 'Livingroom door 1b open', 'address': '6/4/2', 'data_type_id': 2, 'current_value': None},
    {'name': 'Kitchen door 1a open', 'address': '6/4/3', 'data_type_id': 2, 'current_value': None},
    {'name': 'Kitchen door 1b open', 'address': '6/4/4', 'data_type_id': 2, 'current_value': None},
    {'name': 'Bedroom door 1 open', 'address': '6/4/5', 'data_type_id': 2, 'current_value': None},
    {'name': 'Bedroom door 2a open', 'address': '6/4/6', 'data_type_id': 2, 'current_value': None},
    {'name': 'Technical room door open', 'address': '6/4/8', 'data_type_id': 2, 'current_value': None},
    {'name': 'ICEM door open', 'address': '6/4/9', 'data_type_id': 2, 'current_value': None},

    # RESEARCHDATA
    # Powertags

    {'name': 'Bedroom powertag (kW)', 'address': '6/5/4', 'data_type_id': 15, 'current_value': None},
    {'name': 'Laadpaal powertag (kW)', 'address': '6/5/9', 'data_type_id': 15, 'current_value': None},
    {'name': 'Washing machine powertag (kW)', 'address': '6/5/14', 'data_type_id': 15, 'current_value': None},
    {'name': 'Dish washer powertag (kW)', 'address': '6/5/19', 'data_type_id': 15, 'current_value': None},
    {'name': 'Living room powertag (kW)', 'address': '6/5/24', 'data_type_id': 15, 'current_value': None},
    {'name': 'Oven powertag (kW)', 'address': '6/5/29', 'data_type_id': 15, 'current_value': None},
    {'name': 'Pumps powertag (kW)', 'address': '6/5/34', 'data_type_id': 15, 'current_value': None},
    {'name': 'Cooking top powertag (kW)', 'address': '6/5/39', 'data_type_id': 15, 'current_value': None},
    {'name': 'PV powertag (kW)', 'address': '6/5/44', 'data_type_id': 15, 'current_value': None},
    {'name': 'Toilet pump (kW)', 'address': '6/5/49', 'data_type_id': 15, 'current_value': None},
    {'name': 'PV omvormer powertag  (kW)', 'address': '6/5/54', 'data_type_id': 15, 'current_value': None},
    {'name': 'Boiler powertag (kW)', 'address': '6/5/59', 'data_type_id': 15, 'current_value': None},
    {'name': 'Cooking bottom  powertag (kW)', 'address': '6/5/64', 'data_type_id': 15, 'current_value': None}
]

# Delete database file if it exists currently
if os.path.exists('./app.db'):
    os.remove('./app.db')

# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for dataType in DATATYPES:
    dt = DataType(name=dataType)
    db.session.add(dt)

for consumptionType in CONSUMPTIONTYPES:
    ct = ConsumptionType(name=consumptionType['name'], data_type_id=consumptionType['data_type_id'])
    db.session.add(ct)

for script in SCRIPTS:
    spt = Script(name=script['name'])
    db.session.add(spt)

for obj in OBJECTS:
    if 'script_id' in obj:
        spt_id = obj['script_id']
    else:
        spt_id = None
    o = Object(name=obj['name'], current_value=obj['current_value'], address=obj['address'], data_type_id=obj['data_type_id'], script_id=spt_id)

    db.session.add(o)

db.engine.execute('CREATE TABLE `event` ( \
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
        `object_id`	INTEGER NOT NULL, \
        `time`	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
        `value`	INTEGER \
);')  # Needs to be manual since we don't need it in the API

db.session.commit()

# Lets create all devices at the endpoint

item_endpoint = 'http://172.20.10.3:5000/api/v1/items'
usage_endpoint = 'http://172.20.10.3:5000/api/v1/usages'
events_endpoint = 'http://172.20.10.3:5000/api/v1/events'

index = 0
DO_OBJECTS = {0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8}

for objects in OBJECTS:
    # Create item in API
    if index in DO_OBJECTS:
        payload = {'name': OBJECTS[index]["name"], 'comment': 'test'}
        item_request = requests.post(item_endpoint, data=payload)
        print(item_request)
        item_response = json.loads(item_request.text)
        print(item_response)

        # Create usage in API
        usage_request = requests.post(usage_endpoint, {'item_id': item_response['id'],
                                                       'external_item_id': index+1,
                                                       'consumption_type': 'KILOWATT',
                                                       'consumption_amount': 10,
                                                       'address': OBJECTS[index]['address'],
                                                       'unit': 'TOGGLE'})
        usage_response = json.loads(usage_request.text)

    index += 1
