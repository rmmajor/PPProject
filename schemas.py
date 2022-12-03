from flask_bcrypt import generate_password_hash
from marshmallow import validate, Schema, fields


class UserToDo(Schema):
    username = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    email = fields.Email(validate=validate.Email())
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )
    phone = fields.Integer()
    role = fields.String()


class UserData(Schema):
    id = fields.Integer()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email(validate=validate.Email())
    phone = fields.Integer()
    role = fields.String()


class EventToDo(Schema):
    name = fields.String()
    address = fields.String()
    datatime = fields.String()
    tickets_count = fields.Integer()


class EventData(Schema):
    id = fields.Integer()
    name = fields.String()
    address = fields.String()
    datatime = fields.String()
    tickets_count = fields.Integer()


class TicketToDo(Schema):
    seat = fields.Integer()
    type = fields.String()
    user_id = fields.Integer()
    event_id = fields.Integer()


class TicketData(Schema):
    id = fields.Integer()
    seat = fields.Integer()
    type = fields.String()
    user_id = fields.Integer()
    event_id = fields.Integer()

