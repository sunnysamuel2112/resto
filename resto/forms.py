
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
import wtforms
from wtforms import validators
from wtforms.fields.datetime import DateField, TimeField

from wtforms.validators import Length, EqualTo, DataRequired, NumberRange, Email, ValidationError
from resto.models import user, menu ,emp


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        formuser = user.query.filter_by(
            user_name=username_to_check.data).first()
        if formuser:
            raise ValidationError(
                'Username already exists! try a different one.')

    def validate_useremail(self, useremail_to_check):
        formuser = user.query.filter_by(
            user_email=useremail_to_check.data).first()
        if formuser:
            raise ValidationError(
                'User Email already exists! try a different one.')

    def validate_userphno_size(self, field):
        formuser = user.query.filter_by(
            user_phno=field.data).first()
        if formuser:
            raise ValidationError('User Phone Number already exists')
        elif len(str(field.data)) != 10:
            raise ValidationError('Invalid Phone number')

    username = StringField('User Name:', validators=[
                           DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password :', validators=[
                             DataRequired(), Length(min=8)])
    confirmpassword = PasswordField(
        'Confirm Password :', validators=[EqualTo('password')])
    userphno = IntegerField('Phone No :', validators=[
                            DataRequired(), validate_userphno_size])

    useremail = StringField(
        'Customer E-Mail :', validators=[DataRequired(), Email()])
    submit = SubmitField('CREATE ACCOUNT')


class menuForm(FlaskForm):
    def validate_dishname(self, field):
        dishexist = menu.query.filter_by(dish_name=field.data).first()
        if dishexist:
            raise ValidationError('Dish Name Already exists!!!')

    def validate_dishdesc(self, field):
        dishdescexist = menu.query.filter_by(dish_desc=field.data).first()
        if dishdescexist:
            raise ValidationError('Dish Description Already exists!!!')

    dishname = StringField('DISH NAME:', validators=[
                           DataRequired(), Length(min=3, max=30)])
    dishprice = IntegerField('DISH PRICE :', validators=[DataRequired(),
                             NumberRange(min=10, max=1000)])
    dishdesc = StringField('DISH DESCRIPTION:', validators=[
                           DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('ADD DISH')


class reservationForm(FlaskForm):

    def validate_customerphno(self, field):
        if len(str(field.data)) != 10:
            raise ValidationError('Invalid Phone number.')

    def validate_reserveheadcount(form, field):
        if field.data > 5:
            raise ValidationError(
                'Only 5 people allowed due to Covid-19 Guidelines.')
        elif field.data < 1:
            raise ValidationError('Invalid Headcount.')

    customername = StringField('Customer Name', validators=[DataRequired(),
                               Length(min=1, max=30)])
    customeremail = StringField(
        'Customer E-Mail', validators=[DataRequired(), Email()])
    customerphno = IntegerField('Customer PhNo', validators=[
                                DataRequired()])
    reservedate = DateField(
        'Reservation Date', validators=[DataRequired() ])
    reservetime = TimeField(
        'Reservation Time', validators=[DataRequired()])
    reserveheadcount = IntegerField('Head Count', validators=[DataRequired()])
    reservecontent = StringField(
        'additional info can be specified here', validators=[Length(min=0, max=1000)])
    reservesubmit = SubmitField('Book a Table')


class loginForm(FlaskForm):
    loginusername = StringField('User Name', validators=[
        DataRequired()])
    loginpassword = PasswordField('Password', validators=[
        DataRequired()])
    submit = SubmitField('LOGIN')
    
    
'''
    def validate_loginusername(form, field):
        fetchedusers = user.query.filter_by(user_name=field.data).first()
        if fetchedusers:
            raise ValidationError('Invalid User Name')
    def validate_loginpassword(form, field):
        fetcheduser = user.query.filter_by(user_name=field.data).first()
        fetchedpassword = user.query.filter_by(user_pass=field.data).first()
        if field.data == fetcheduser.user_name:
            if field.data != fetcheduser.user_pass:
                raise ValidationError('Invalid Password')
'''
            


class AddDishForm(FlaskForm):
    submit = SubmitField('Add')
    
    
class updatedishForm(FlaskForm):
    def validate_dishname(self, field):
        dishexist = menu.query.filter_by(dish_name=field.data).first()
        if dishexist:
            raise ValidationError('Dish Name Already exists!!!')

    def validate_dishdesc(self, field):
        dishdescexist = menu.query.filter_by(dish_desc=field.data).first()
        if dishdescexist:
            raise ValidationError('Dish Description Already exists!!!')

    dishname = StringField('DISH NAME:', validators=[
                           DataRequired(), Length(min=3, max=30)])
    dishprice = IntegerField('DISH PRICE :', validators=[DataRequired(),
                             NumberRange(min=10, max=1000)])
    dishdesc = StringField('DISH DESCRIPTION:', validators=[
                           DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('UPDATE')
    
class DishcountForm(FlaskForm):
    quantity = IntegerField('quantity', validators=[DataRequired(),
                             NumberRange(min=1)])
    submit = SubmitField('ADD')
    
    
    
    
class addEmpForm(FlaskForm):
    
    def validate_empphno_size(self, field):
        empuser = emp.query.filter_by(
            emp_phno=field.data).first()
        if empuser:
            raise ValidationError('Phone Number already exists')
        elif len(str(field.data)) != 10:
            raise ValidationError('Invalid Phone number')
                                  
    empname = StringField('Name:', validators=[
                           DataRequired(), Length(min=3, max=30)])
    empdesg = StringField('Designation:', validators=[
                           DataRequired(), Length(min=3, max=30)])
    empphno = IntegerField('Phone No :', validators=[
                            DataRequired(), validate_empphno_size])
    empsalary = IntegerField('Salary :', validators=[
                            DataRequired()])
    empaddress = StringField(
        'Address', validators=[DataRequired()])
    submit = SubmitField('ADD')
    
    
class placeOrdForm(FlaskForm):
    submit = SubmitField('PLACE ORDER')