import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))
"""string: Base directory
"""

connex_app = connexion.App(__name__, specification_dir=basedir + '/endpoint_config')
"""zalando connexion plugin
"""

app = connex_app.app

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

from classes.simulation.SimulationController import SimulationController

USE_SIMULATION = True  # Simulation global
"""boolean
"""
SIM_REGISTER_FROM_DATABASE = True
"""boolean: Register devices from database
"""
SIM_CONTROLLER = SimulationController()
"""Initialized Simulation controller
"""
