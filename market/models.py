from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

class user(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship("item", backref="owned_user", lazy=True)

    @property
    def pretty_budget(self):
        if(len(str(self.budget)) >= 4):
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}$"
        else:
            return f"{self.budget}$"

    # @property
    # def password(self):
    #     return self.password

    # @password.setter
    # def password(self, plain_text_password):
    #     self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def check_password(self, attempted_password):
        # return bcrypt.check_password_hash(self.password_hash, attempted_password)
        return self.password_hash == attempted_password

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

class item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(15), nullable=False, unique=True)
    description = db.Column(db.String(1000))
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Name : {self.name}"

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()


#  from market import items
#  db.create_all()
#  from market.models import db 
#  item1 = item(name="Iphone", price=500, barcode=1234567890, description="desc")   
#  db.session.add(item1)    
#  db.session.commit()