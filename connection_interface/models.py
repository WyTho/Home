from config import db, ma


class ConsumptionType(db.Model):
    """Consumption type for database model
    
    Arguments:
        db {SQLAlchemy} -- SQLAlchemy config
    """
    __tablename__ = "consumption_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    data_type_id = db.Column(db.Integer, db.ForeignKey('data_type.id'), nullable=False)


class ConsumptionTypeSchema(ma.ModelSchema):
    """Marshmellow ConsumptionType
    
    Arguments:
        ma {Marshmellow} -- Marshmellow config
    """

    class Meta:
        model = ConsumptionType
        sqla_session = db.session


class Script(db.Model):
    """Script for database model
    
    Arguments:
        db {SQLAlchemy} -- SQLAlchemy config
    """
    __tablename__ = "script"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Object(db.Model):
    """Object for database model
    
    Arguments:
        db {SQLAlchemy} -- SQLAlchemy config
    """
    __tablename__ = "object"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(10), nullable=False)
    data_type_id = db.Column(db.Integer, db.ForeignKey('data_type.id'), nullable=False)
    current_value = db.Column(db.String(), nullable=True)
    script_id = db.Column(db.Integer, db.ForeignKey('script.id'), nullable=True)


class ObjectSchema(ma.ModelSchema):
    """Marshmellow Object Schema
    
    Arguments:
        ma {Marshmellow} -- Marshmellow config
    """

    class Meta:
        model = Object
        fields = ["id", "name", "address", "data_type_id", "current_value"]
        sqla_session = db.session


class DataType(db.Model):
    """Datatype for database model
    
    Arguments:
        db {SQLAlchemy} -- SQLAlchemy config
    """
    __tablename__ = "data_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)


class DataTypeSchema(ma.ModelSchema):
    """Datatype marshmellow schema
    
    Arguments:
        ma {Marshmellow} -- Marshmellow config
    """

    class Meta:
        model = DataType
        sqla_session = db.session
