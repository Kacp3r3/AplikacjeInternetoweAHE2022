from market import db
from market.models import Item, User


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    user1 = User(username="Kacper", email="ex@ex.com", password_hash="###")
    db.session.add(user1)
    db.session.commit()
    db.session.add(Item(name="Samsung S10e", price = 2500, barcode="123456789012", description="Nope", owner=user1.id ))
    db.session.add(Item(name="Samsung S10", price = 3500, barcode="326426789012", description="Nope" ))
    db.session.commit()