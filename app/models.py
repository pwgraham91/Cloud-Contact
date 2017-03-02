from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    number = db.Column(db.String(64))
    note = db.Column(db.VARCHAR)

    user = db.relationship("User", backref="phone_numbers")


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email_address = db.Column(db.String(120))
    note = db.Column(db.VARCHAR)

    user = db.relationship("User", backref="email_addresses")


class Addresses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    street = db.Column(db.VARCHAR)
    street_2 = db.Column(db.VARCHAR)
    city = db.Column(db.VARCHAR)
    state = db.Column(db.String(64))
    country = db.Column(db.String(64))
    zip_code = db.Column(db.String(64))
    note = db.Column(db.VARCHAR)

    user = db.relationship("User", backref="addresses")
