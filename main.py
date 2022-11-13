from flask import Flask, request, jsonify, json
from marshmallow import ValidationError
from sqlalchemy import exc
import util_func

import db_util
from schemas import *
from models import *


app = Flask(__name__)


# Створює подію


@app.route("/event", methods=["POST"])
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


# Інші методи для події


@app.route("/event/<int:idevent>", methods=["DELETE", "PUT", "GET"])
def event_methods(idevent):
    if request.method == "PUT":
        try:
            event_data = EventToDo().load(request.json)
            event = db_util.get_entry_byid(Event, idevent)

            if 'datatime' in event_data and \
                    not util_func.check_if_past_time(event_data['datatime']):       # Перевірка на час події
                return "Error400: This is not proper date", 400
            else:
                db_util.update_entry(event, **event_data)
                return "Event's updated", 200

        except exc.NoResultFound:                                     # Якщо користувач не знайдений
            return jsonify("Error404: Event not found"), 404
        except ValidationError as err:
            return str(err), 400
    elif request.method == "DELETE":
        try:
            int(idevent)                                                 # реалізоване каскадне виділення
            ticket_list = db_util.get_tickets_by(Ticket, idevent)
            for i in ticket_list:
                db_util.delete_entry(Ticket, i.id)
            db_util.delete_entry(Event, idevent)
            return "Event and event's tickets are deleted", 200
        except exc.NoResultFound:
            return jsonify("Error404: Event not found"), 404
    else:
        try:
            event = db_util.get_entry_byid(Event, idevent)
            return jsonify(EventData().dump(event))
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


# Створення квитка


@app.route("/ticket", methods=["POST"])
def ticket():
    try:
        ticket_data = TicketToDo().load(request.json)

        event_tickets = db_util.get_tickets_by(Ticket, ticket_data['event_id'])         # Перевірка, чи не зайняте місце
        for i in event_tickets:
            if ticket_data['seat'] == i.seat:
                return jsonify("Error409: Seat is already used"), 409
        if ticket_data['type'] != 'reserved' or ticket_data['type'] != 'bought':        # Перевірка на правильність типу
            return jsonify("Error409: Wrong ticket type"), 409                          # квитка
        t_ticket = db_util.create_entry(Ticket, **ticket_data)
        return jsonify(TicketData().dump(t_ticket))
    except ValidationError as err:
        return str(err), 400


# Методи для квитка


@app.route("/ticket/<int:tid>", methods=["DELETE", "PUT"])
def tick_id(tid):
    if request.method == "PUT":
        try:
            ticket_data = TicketToDo().load(request.json)

            if 'type' in ticket_data:
                if ticket_data['type'] != 'reserved' and ticket_data['type'] != 'bought':    # Перевірка на правильність
                    return jsonify("Error409: Wrong ticket type"),                           # типу квитка

            t_ticket = db_util.get_entry_byid(Ticket, tid)
            event_tickets = db_util.get_tickets_by(Ticket, t_ticket.event_id)
            for i in event_tickets:                                                          # І чи не зайняте місце
                if ticket_data['seat'] == i.seat and t_ticket.id != i.id:
                    return jsonify("Error409: Seat is already used"), 409

            db_util.update_entry(t_ticket, **ticket_data)
            return "Ticket's updated", 200
        except exc.NoResultFound:
            return jsonify("Error404: Ticket not found"), 404
        except ValidationError as err:
            return str(err), 400
    elif request.method == "DELETE":
        try:
            db_util.delete_entry(Ticket, tid)
            return "User's deleted", 200
        except exc.NoResultFound:
            return jsonify("Error404: Ticket not found"), 404


# Створеня користувача


@app.route("/user", methods=["POST"])
def user():
    try:
        user_data = UserToDo().load(request.json)
        t_user = db_util.create_entry(User, **user_data)
        return jsonify(UserData().dump(t_user))
    except ValidationError as err:          # Може вибити, якщо вказані не унікальні ім'я користувача, email і номер
        return str(err), 400                # телефону


@app.route("/user/login", methods=["POST"])
def log_user():
    return 'log'


@app.route("/user/logout", methods=["POST"])
def logout():
    return 'log_out'


# Методи для користувача за його ім'ям користувача


@app.route("/user/<string:username>", methods=["GET", "PUT", "DELETE"])
def user_id(username):
    if request.method == "GET":
        try:
            t_user = db_util.get_entry_by_username(User, username)
            return jsonify(UserData().dump(t_user))
        except exc.NoResultFound:
            return jsonify("Error404: User not found"), 404
    elif request.method == "PUT":
        try:
            user_data = UserToDo().load(request.json)
            t_user = db_util.get_entry_by_username(User, username)
            db_util.update_entry(t_user, **user_data)
            return "User update", 200
        except exc.NoResultFound:
            return jsonify("Error404: User not found"), 404
        except ValidationError as err:                          # Такі ж можливі помилки, як у post-методі
            return str(err), 400
    else:
        try:
            user_tickets = db_util.get_tickets_by(Ticket, username)        # Каскадне видалення зі всіма квитками
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


if __name__ == '__main__':
    app.run(debug=True)
