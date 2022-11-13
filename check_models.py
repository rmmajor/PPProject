from models import *


user1 = User(id=1, username='user1', firstname='Qwer', lastname='asd',
             email='qwer@gmail.com', password='123', phone='380965115657', role='user')
user2 = User(id=2, username='user2', firstname='Qwer', lastname='asd',
             email='qwe124r@gmail.com', password='123', phone='380964515657', role='user')
Session.add(user1)
Session.add(user2)
Session.commit()

event1 = Event(name="LGBTQC++ meeting", address='ddszdxd', datatime='2022-01-05 10:10:10', tickets_count='150')
event2 = Event(name="rave", address="asdadas", datatime='2022-06-05 11:11:11', tickets_count='170')
Session.add(event1)
Session.add(event2)
Session.commit()

ticket1 = Ticket(id=1, seat=12, type='reserved', user_id='1', event_id='1')
ticket2 = Ticket(id=2, seat=19, type='bought', user_id='2', event_id='1')
ticket3 = Ticket(id=3, seat=89, type='bought', user_id='2', event_id='2')
Session.add(ticket1)
Session.add(ticket2)
Session.add(ticket3)
Session.commit()
Session.close()
