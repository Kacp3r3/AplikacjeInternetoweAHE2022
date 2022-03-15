from market import db

class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(30), nullable = False, unique = True)
    price = db.Column(db.Integer(), nullable = False)
    barcode = db.Column(db.String(12), nullable = False, unique = True)
    description = db.Column(db.String(1024), nullable = False)
    owner = db.Column(db.Integer(), db.ForeignKey("users.id"))

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    password_hash = db.Column(db.String(60), nullable = False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship("Item", backref="owned_user", lazy=True)