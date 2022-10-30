from models import *

session = Session

user1 = user(iduser=1, username='user1', firstname='Qwer', lastname='asd',
             email='qwer@gmail.com', password='123', phone='380964515657', role='user')
user2 = user(iduser=2, username='user1', firstname='Qwer', lastname='asd',
             email='qwer@gmail.com', password='123', phone='380964515657', role='user')
session.add(user1)
session.add(user2)
session.commit()

event1 = event(idevent=1, adress='ddszdxd', datatime='2022-01-05', tikets_count='150')
event2 = event(idevent=2, adress='rdsvdv', datatime='2022-06-05', tikets_count='170')
session.add(event1)
session.add(event2)
session.commit()

ticket1 = ticket(idticket=1, seat=12, type='RESERVET', user_id='1', event_id='1')
ticket2 = ticket(idticket=2, seat=19, type='ewvrwerv', user_id='2', event_id='1')
ticket3 = ticket(idticket=3, seat=89, type='jnuyjn', user_id='2', event_id='2')
session.add(ticket1)
session.add(ticket2)
session.add(ticket3)
session.commit()
session.close()
