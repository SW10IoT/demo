from demo import db
from demo import User


db.create_all()

def add_user(name, password, email):
    u = User(name, password, email)
    db.session.add(u)


add_user('Peter', '123456', 'peter@peter.com')
add_user('Claus', 'pass123', 'claus@claus.com')
add_user('Stefan', '1337', 'stefan@stefan.com')
add_user('Rene', 'j363r53j', 'rene@rene.com')

db.session.commit()
