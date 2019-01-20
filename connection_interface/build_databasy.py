import os
from config import db
from models import Object, ConsumptionType, DataType

DATATYPES = [
    "1 byte signed integer",    # 1
    "1-bit(boolean)",           # 2
    "1 byte unsigned integer",  # 3
    "1-byte ASCII-character",   # 4
    "2 byte floating point",    # 5
    "2 byte signed integer",    # 6
    "2 byte unsigned integer",  # 7
    "2-bits(1 evaluated bit)",  # 8
    "3 byte date",              # 9
    "3 byte time/day",          # 10
    "3 byte unsigned integer",  # 11
    "4 byte accesscontrol",     # 12
    "4 byte floating point",    # 13
    "4 byte signed integer",    # 14
    "4 byte unsigned integer",  # 15
    "4-bits(3 evaluated bits)", # 16
    "8 byte signed integer",    # 17
    "14 byte ASCII",            # 18
    "250 byte data"             # 19
]

CONSUMPTIONTYPES = [
    {'name': 'scale', 'data_type_id': 2},       # 1
    {'name': 'angle', 'data_type_id': 2},       # 2
    {'name': 'toggle', 'data_type_id': 1},      # 3
    {'name': 'activate', 'data_type_id': 1},    # 4
    {'name': 'transition', 'data_type_id': 1},  # 5
    {'name': 'alarm', 'data_type_id': 1},       # 6
    {'name': 'low/high', 'data_type_id': 1},    # 7
    {'name': 'step', 'data_type_id': 1},        # 8
    {'name': 'move up/move down', 'data_type_id': 1},   #9
    {'name': 'open/close', 'data_type_id': 1},          #10
    {'name': 'start/stop', 'data_type_id': 1},          #11
    {'name': 'activity', 'data_type_id': 1},            #12
    {'name': 'inversion', 'data_type_id': 1},           #13
    {'name': 'type dimming', 'data_type_id': 1},        #14
    {'name': 'data', 'data_type_id': 1},                #15
    {'name': 'temperature', 'data_type_id': 4},         #16
    {'name': '232.600 RGB Color', 'data_type_id': 10},  #17
    {'name': 'step dimming/blinds', 'data_type_id': 15},#18
    {'name': '14 byte HEX', 'data_type_id': 17}         #19
]

OBJECTS = [
    {'name': 'Badkamer Spots', 'address': '0/0/1', 'consumption_type_id': 3, 'current_value': None},
    {'name': 'Badkamer Spots', 'address': '0/2/1', 'consumption_type_id': 18, 'current_value': None},

    {'name': 'Gang lamp', 'address': '0/0/2', 'consumption_type_id': 3, 'current_value': None},
    {'name': 'Gang lamp', 'address': '0/2/2', 'consumption_type_id': 18, 'current_value': None},

    {'name': 'Bed left', 'address': '0/0/3', 'consumption_type_id': 3, 'current_value': None},
    {'name': 'Bed left', 'address': '0/2/3', 'consumption_type_id': 18, 'current_value': None},

    {'name': 'Bed right', 'address': '0/0/4', 'consumption_type_id': 3, 'current_value': None},
    {'name': 'Bed right', 'address': '0/2/4', 'consumption_type_id': 18, 'current_value': None},

    {'name': 'Plafonier slaap', 'address': '0/0/5', 'consumption_type_id': 3, 'current_value': None},
    {'name': 'Plafonier slaap', 'address': '0/2/5', 'consumption_type_id': 18, 'current_value': None},

    {'name': 'Plafoniere woon', 'address': '0/0/6', 'consumption_type_id': 3, 'current_value': None},
    {'name': 'Plafoniere woon', 'address': '0/2/6', 'consumption_type_id': 18, 'current_value': None},

    {'name': 'lamp corner', 'address': '0/0/7', 'consumption_type_id': 3, 'current_value': None},
    {'name': 'lamp corner', 'address': '0/2/7', 'consumption_type_id': 18, 'current_value': None},

    {'name': 'dining table', 'address': '0/0/7', 'consumption_type_id': 3, 'current_value': None},
    {'name': 'dining table', 'address': '0/2/7', 'consumption_type_id': 18, 'current_value': None},

    {'name': 'spots kitchen', 'address': '0/0/7', 'consumption_type_id': 3, 'current_value': None},
    {'name': 'spots kitchen', 'address': '0/2/7', 'consumption_type_id': 18, 'current_value': None},

    {'name': 'Master/slave heating/cooling', 'address': '1/2/0', 'consumption_type_id': 3, 'current_value': None},

    {'name': 'Bedroom (manual)', 'address': '3/1/0', 'consumption_type_id': 8, 'current_value': None},
    {'name': 'Bedroom (Auto)', 'address': '3/1/1', 'consumption_type_id': 8, 'current_value': None},
    {'name': 'Living (manual)', 'address': '3/1/2', 'consumption_type_id': 8, 'current_value': None},
    {'name': 'Living (Auto)', 'address': '3/1/3', 'consumption_type_id': 8, 'current_value': None},
    {'name': 'Kitchen (manual)', 'address': '3/1/4', 'consumption_type_id': 8, 'current_value': None},
    {'name': 'Kitchen (Auto)', 'address': '3/1/5', 'consumption_type_id': 8, 'current_value': None},
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

for obj in OBJECTS:
    o = Object(name=obj['name'], address=obj['address'], consumption_type_id=obj['consumption_type_id'])
    db.session.add(o)

db.session.commit()