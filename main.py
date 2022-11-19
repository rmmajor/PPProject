from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import Flask, request, jsonify, make_response
from flask_bcrypt import check_password_hash
from marshmallow import ValidationError
from functools import wraps
from sqlalchemy import exc

from schemas import *
from models import *
import util_func
import db_util


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # хз шо це, без нього не паше
jwt = JWTManager(app)


def validate_user():
    def wrapper(fn):
        @wraps(fn)
        def decorator(username):
            try:
                verify_jwt_in_request()
                current_identity_username = get_jwt_identity()
                params = get_jwt()
                user = db_util.get_entry_by_username(User, username=username)

                if user.username != current_identity_username and params["role"] != "admin":
                    return jsonify({"Error": "Acces denied"}), 401

                return fn(username)

            except exc.NoResultFound:
                return jsonify({"Error": "Acces denied"}), 401

        return decorator

    return wrapper


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            params = get_jwt()
            if params["role"] == 'admin':
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper


# Створеня користувача
@app.route("/user", methods=["POST"])
def user():
    try:
        user_data = UserToDo().load(request.json)
        t_user = db_util.create_entry(User, **user_data)
        return jsonify(UserData().dump(t_user))
    except ValidationError as err:          # Може вибити, якщо вказані не унікальні ім'я користувача, email і номер
        return str(err), 400                # телефону
    except exc.IntegrityError as err:
        return jsonify({"Error": "User already exists"}), 400


@app.route("/user/login", methods=["POST"])
def login_user():
    try:
        auth = request.authorization
        user = db_util.get_entry_by_username(User, auth.username)

        if check_password_hash(user.password, auth.password):
            access_token = create_access_token(
                identity=user.username,
                additional_claims= {'role': str(user.role)}
            )

            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'Error': 'Wrong password'}), 401

    except exc.NoResultFound:
        return jsonify("Error404: User not found"), 404

    except UnicodeEncodeError:
        return jsonify({'Error': 'Wrong password'}), 401


@app.route("/user/<string:username>", methods=["GET"])
@validate_user()
def get_user_by_username(username):
    try:
        t_user = db_util.get_entry_by_username(User, username)
        return jsonify(UserData().dump(t_user))
    except exc.NoResultFound:
        return jsonify("Error404: User not found"), 404


@app.route("/user/<string:username>", methods=["PUT"])
@validate_user()
def upd_user_by_username(username):
    try:
        user_data = UserToDo().load(request.json)
        t_user = db_util.get_entry_by_username(User, username)
        db_util.update_entry(t_user, **user_data)
        return "User update", 200
    except exc.NoResultFound:
        return jsonify("Error404: User not found"), 404
    except ValidationError as err:
        return str(err), 400
    except exc.IntegrityError as err:
        return jsonify("User already exists"), 400


@app.route("/user/<string:username>", methods=["DELETE"])
@validate_user()
def delete_user_by_username(username):
    try:
        user_tickets = db_util.get_tickets_by(Ticket, username)  # Каскадне видалення зі всіма квитками
        for i in user_tickets:
            db_util.delete_entry(Ticket, i.id)
        db_util.delete_entry_by_username(User, username)
        return "User and user's tickets are deleted", 200
    except exc.NoResultFound:
        return jsonify("Error404: User not found"), 404


# Шукає всі квитки для користувача з ніком
@app.route("/user/<string:username>/tickets", methods=["GET"])
def get_user_tick(username):
    try:
        user_tickets = db_util.get_tickets_by(Ticket, username)
        return jsonify(TicketData().dump(user_tickets, many=True))
    except exc.NoResultFound:
        return jsonify("Error404: User not found"), 404


# Створює подію
@app.route("/event", methods=["POST"])
@admin_required()
def post_event():
    try:
        event_data = EventToDo().load(request.json)
        if util_func.check_if_past_time(event_data['datatime']):    # Перевірка чи вказана дата не є
            t_event = db_util.create_entry(Event, **event_data)     # минулою, сьогоднішньою та не через 10 років
            return jsonify(EventData().dump(t_event))
        else:
            return "Error400: This is not proper date", 400
    except ValidationError as err:                                  # Може вибити, якщо ім'я події повторюється
        return str(err), 400
    except exc.IntegrityError as err:
        return jsonify("Event already exists"), 400


@app.route("/event/<int:idevent>", methods=["GET"])
def get_event(idevent):
    try:
        event = db_util.get_entry_byid(Event, idevent)
        return jsonify(EventData().dump(event))
    except exc.NoResultFound:
        return jsonify("Error404: Event not found"), 404


@app.route("/event/<int:idevent>", methods=["PUT"])
@admin_required()
def upd_event(idevent):
    try:
        event_data = EventToDo().load(request.json)
        event = db_util.get_entry_byid(Event, idevent)

        if 'datatime' in event_data and \
                not util_func.check_if_past_time(event_data['datatime']):  # Перевірка на час події
            return "Error400: This is not proper date", 400
        else:
            db_util.update_entry(event, **event_data)
            return "Event's updated", 200

    except exc.NoResultFound:  # Якщо користувач не знайдений
        return jsonify("Error404: Event not found"), 404

    except ValidationError as err:
        return str(err), 400


@app.route("/event/<int:idevent>", methods=["DELETE"])
@admin_required()
def delete_event(idevent):
    try:
        int(idevent)  # реалізоване каскадне виділення
        ticket_list = db_util.get_tickets_by(Ticket, idevent)
        for i in ticket_list:
            db_util.delete_entry(Ticket, i.id)
        db_util.delete_entry(Event, idevent)
        return "Event and event's tickets are deleted", 200
    except exc.NoResultFound:
        return jsonify("Error404: Event not found"), 404


# Знаходить всі куплені або зарезервовані квитки для події
@app.route("/event/<int:eid>/tickets", methods=["GET"])
def get_event_ticket(eid):
    try:
        eid = int(eid)
        ticket_list = db_util.get_tickets_by(Ticket, eid)
        return jsonify(TicketData().dump(ticket_list, many=True))
    except exc.NoResultFound:
        return jsonify("Error404: Event not found"), 404


# Методи для квитка
@app.route("/ticket", methods=["POST"])
@admin_required()
def ticket():
    try:
        ticket_data = TicketToDo().load(request.json)

        event_tickets = db_util.get_tickets_by(Ticket, ticket_data['event_id'])         # Перевірка, чи не зайняте місце

        for i in event_tickets:
            if ticket_data['seat'] == i.seat:
                return jsonify("Error409: Seat is already used"), 409

        if ticket_data['type'] not in ['reserved', 'bought']:        # Перевірка на правильність типу
            return jsonify("Error409: Wrong ticket type"), 409                          # квитка

        t_ticket = db_util.create_entry(Ticket, **ticket_data)
        return jsonify(TicketData().dump(t_ticket))

    except ValidationError as err:
        return str(err), 400


@app.route("/ticket/<int:tid>", methods=["PUT"])
@admin_required()
def ticket_upd(tid):
    try:
        ticket_data = TicketToDo().load(request.json)

        if 'type' in ticket_data:
            if ticket_data['type'] != 'reserved' and ticket_data['type'] != 'bought':  # Перевірка на правильність
                return jsonify("Error409: Wrong ticket type"), 405  # типу квитка

        t_ticket = db_util.get_entry_byid(Ticket, tid)
        event_tickets = db_util.get_tickets_by(Ticket, t_ticket.event_id)
        for i in event_tickets:  # І чи не зайняте місце
            if ticket_data['seat'] == i.seat and t_ticket.id != i.id:
                return jsonify("Error409: Seat is already used"), 409

        db_util.update_entry(t_ticket, **ticket_data)
        return "Ticket's updated", 200

    except exc.NoResultFound:
        return jsonify("Error404: Ticket not found"), 404
    except ValidationError as err:
        return str(err), 400


@app.route("/ticket/<int:tid>", methods=["DELETE"])
@admin_required()
def ticket_delete(tid):
    try:
        db_util.delete_entry(Ticket, tid)
        return "User's deleted", 200
    except exc.NoResultFound:
        return jsonify("Error404: Ticket not found"), 404


if __name__ == '__main__':
    app.run(debug=True, port=8080)
