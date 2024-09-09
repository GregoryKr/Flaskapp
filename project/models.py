from project import db

# class User(database users)
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    addresses = db.relationship('Address', backref='user', lazy=True)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}


class Address(db.Model):
    # __tablename__ = 'addresses'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                          nullable=False)

    def __str__(self):
        return f'address: {self.address}, id: {self.id}, person_id: {self.person_id}'

    def json(self):
        return {'id': self.id, 'address': self.address, 'person_id': self.person_id}
