import json

from models import *


# Базовані методи


def create_entry(model_class, *, commit=True, **kwargs):        # Для постів
    session = Session()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return entry


def get_entry_byid(model_class, id, **kwargs):                  # Для пошуків за ід
    session = Session()
    return session.query(model_class).filter_by(id=id, **kwargs).one()


def get_tickets_by(model_class, param, **kwargs):               # Виводить всі квитки для івенту за ід, або для
    session = Session()                                         # користувача за нікнеймом
    if isinstance(param, int):
        return session.query(model_class).filter_by(event_id=param, **kwargs).all()
    else:
        user = get_entry_by_username(User, param)
        return session.query(model_class).filter_by(user_id=user.id, **kwargs).all()


def get_entry_by_username(model_class, username, **kwargs):     # Вивід користувача за нікнеймом
    session = Session()
    return session.query(model_class).filter_by(username=username, **kwargs).one()


def update_entry(entry, *, commit=True, **kwargs):      # Для путів
    session = Session()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    else:
        return entry


def delete_entry(model_class, id, *, commit=True, **kwargs):       # Для делітів
    session = Session()
    session.query(model_class).filter_by(id=id, **kwargs).delete()
    if commit:
        session.commit()


def delete_entry_by_username(model_class, username, *, commit=True, **kwargs):  # Видаляє за ніком юзера
    session = Session()
    session.query(model_class).filter_by(username=username, **kwargs).delete()
    if commit:
        session.commit()


