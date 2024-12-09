from . import db


class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    code = db.Column(db.String(3), nullable=False, unique=True)

    def __repr__(self):
        return f'<Country {self.name}>'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)

    country = db.relationship('Country', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'
