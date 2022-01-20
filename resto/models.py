from datetime import datetime
from enum import unique
from resto import db

# models
# model creation


class customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True)
    cust_name = db.Column(db.String(length=30), nullable=False)
    cust_phno = db.Column(db.Integer, nullable=False, unique=True)
    #cust_email = db.Column(db.String(length=30), nullable=False, unique=True)
    cust_ord_id = db.relationship(
        'order', backref="custord", lazy="select", uselist=False)

    def __repr__(self):
        return f'{self.cust_id , self.cust_name , self.cust_phno}'


class menu(db.Model):
    dish_id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(length=30), nullable=False, unique=True)
    dish_price = db.Column(db.Integer, nullable=False)
    dish_desc = db.Column(db.String(length=100), nullable=False, unique=True)
    menu_ord_id = db.relationship(
        'order', backref="menuord", lazy="select", uselist=False)

    def __repr__(self):
        return f'{self.dish_id , self.dish_name , self.dish_price , self.dish_desc}'


class order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    ord_cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))
    ord_dish_id = db.Column(db.Integer, db.ForeignKey('menu.dish_id'))
    ord_dish_count = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.order_id , self.ord_cust_id , self.ord_dish_id , self.ord_dish_count}'


""" 
    ord_bill_id = db.relationship(
        'bill', backref="ordbill", lazy="select", uselist=False)
class bill(db.Model):
    bill_id = db.Column(db.Integer, primary_key=True)
    bill_ord_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    bill_amt = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.bill_id , self.bill_ord_id , self.bill_amt}'

 """


class emp(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(length=30),
                         nullable=False)
    emp_desg = db.Column(db.String(length=30),
                         nullable=False)
    emp_phno = db.Column(db.Integer,
                         nullable=False, unique=True)
    emp_salary = db.Column(db.Integer,
                           nullable=False)
    emp_address = db.Column(db.String(length=100),
                            nullable=False)

    def __repr__(self):
        return f'{self.emp_id , self.emp_name ,self.emp_desg, self.emp_phno,self.emp_salary , self.emp_address}'


class user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(length=30),
                          nullable=False, unique=True)
    user_pass = db.Column(db.String(length=15),
                          nullable=False)
    user_phno = db.Column(db.Integer,
                          nullable=False, unique=True)
    user_email = db.Column(db.String(length=30),
                           nullable=False, unique=True)

    def __repr__(self):
        return f'{ self.user_id , self.user_name , self.user_pass , self.user_phno , self.user_email}'


class reserve(db.Model):
    reserve_id = db.Column(db.Integer, primary_key=True)
    cust_name = db.Column(db.String(length=30),
                          nullable=False)
    cust_email = db.Column(db.String(length=50),
                           nullable=False)
    cust_phno = db.Column(db.Integer,
                          nullable=False)
    reserve_date = db.Column(db.Date, nullable=False)
    reserve_time = db.Column(db.Time, nullable=False)
    reserve_hc = db.Column(db.Integer,
                           nullable=False, default=1)

    reserve_content = db.Column(db.String(length=1000),
                                nullable=True)

    def __repr__(self):
        return f'{ self.reserve_id , self.cust_name , self.cust_email , self.cust_phno , self.reserve_date, self.reserve_time , self.reserve_hc , self.reserve_content}'


db.create_all()
# models


"""bill_cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))bill_dish_id = db.Column(db.Integer, db.ForeignKey('menu.dish_id'))"""

""" 
class admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(length=30),
                           nullable=False, unique=True)
    admin_pass = db.Column(db.String(length=15),
                           nullable=False)
    admin_phno = db.Column(db.Integer,
                           nullable=False, unique=True)
    admin_email = db.Column(db.String(length=30),
                            nullable=False, unique=True)
     """
