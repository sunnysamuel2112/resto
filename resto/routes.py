from flask import flash, request
from sqlalchemy import desc
from resto import app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for
from resto.models import user, order, menu, reserve, emp, customer
from resto.forms import addEmpForm, loginForm, menuForm, RegisterForm, placeOrdForm, reservationForm, AddDishForm, updatedishForm
from resto import db
from flask_mail import Mail, Message

# mailservice
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'restofoodservice@gmail.com'
app.config['MAIL_PASSWORD'] = 'resto@2000'

mail = Mail(app)


# route file
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user2 = user.query.filter_by(user_name=form.loginusername.data).first()
        if form.loginusername.data == 'admin':
            if form.loginpassword.data == 'resto@admin':
                flash('Admin Login Succesfull!!', category="success")
                return redirect(url_for('admin'))
            else:
                flash('Invalid User Name or Password!!', category="danger")
                return redirect(url_for('login'))

        elif user2 is not None and user2.user_name == form.loginusername.data and user2.user_pass == form.loginpassword.data:
            flash('Customer Login Succesfull!!', category="success")
            return redirect(url_for('menucust'))
        else:
            flash('Invalid User Name or Password!!', category="danger")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)





# routes

@app.route('/menu12345')
def menupage():
    menu1 = menu.query.all()
    userquery = user.query.all()
    return render_template('data.html', dishnamesfordisplay=menu1, usersfordisplay=userquery)


@app.route('/admin/insert', methods=['GET', 'POST'])
def menuaddpage():
    dishlist = menu.query.all()
    form = menuForm()
    if form.validate_on_submit():
        dish = menu(dish_name=form.dishname.data,
                    dish_price=form.dishprice.data,
                    dish_desc=form.dishdesc.data)
        db.session.add(dish)
        db.session.commit()
        flash('Dish Added Succesfully!!', category="success")
        return redirect(url_for('menuaddpage'))
    if form.errors != {}:
        for dish_err_msg in form.errors.values():
            flash(f'Failed to Add New Dish: {dish_err_msg}', category="danger")
    return render_template('cusadd_dish.html', toshowdish=dishlist, title='New Dish', form=form)


@app.route('/emp')
def employee():
    empnames = emp.query.all()
    print(empnames)
    return render_template('emp.html', empnamesfordisplay=empnames)


# admin page
@app.route('/admin')
def admin():
    dishlist = menu.query.all()
    return render_template('admin.html', toshowdish=dishlist)


@app.route('/admin/users')
def appuser():
    usernames = user.query.all()
    return render_template('user.html', usernamesfordisplay=usernames)


@app.route('/register', methods=['GET', 'POST'])
def registerpage():
    form = RegisterForm()
    if form.validate_on_submit():
        user1 = user(user_name=form.username.data,
                     user_pass=form.password.data,
                     user_phno=form.userphno.data,
                     user_email=form.useremail.data,
                     )
        newcust = customer(cust_name=form.username.data,
                           cust_phno=form.userphno.data

                           )
        try:
            message = 'Thank you for Registering\nHere is your Login Credentials:\nUsername: %s\nPassword: %s\nLogin using these credentials\nWe hope you eat to your heart\'s content!!!!\n\n\n\nfor further info contact us at 8970514735,\nThank You.' % (
                form.username.data, form.password.data)
            subject = 'Hello from RESTO, %s' % form.username.data
            msg = Message(body=message, subject=subject,
                          sender='restofoodservice@gmail.com', recipients=[form.useremail.data])
            mail.send(msg)
            db.session.add(user1)
            db.session.add(newcust)
            db.session.commit()
            flash('registration succesfull', category="success")
            return redirect(url_for('menucust'))
        except:
            flash('Looks like you dont have Internet', category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error during register: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/about')
def about():
    return render_template('custabout.html')


@app.route('/reserve', methods=['GET', 'POST'])
def reservation():
    form = reservationForm()
    if form.validate_on_submit():
        reservation1 = reserve(
            cust_name=form.customername.data,
            cust_email=form.customeremail.data,
            cust_phno=form.customerphno.data,
            reserve_date=form.reservedate.data,
            reserve_time=form.reservetime.data,
            reserve_hc=form.reserveheadcount.data,
            reserve_content=form.reservecontent.data)

        if reserve.query.count() == 1 or 2 or 3 or 4 or 5:
            try:
                message = f'Hi {form.customername.data},\nThank you for booking your table with RESTO!\nYour reservation for {form.reserveheadcount.data} people on {form.reservedate.data}  is confirmed.\nFor any changes please contact us.\n\nYour Reservation details are:\nName: {form.customername.data}\nPhone Number: {form.customerphno.data}\nDate: {form.reservedate.data}\nTime: {form.reservetime.data}\n\nWe look forward to serving you.\n\nFor further info contact us at : 7019003679,8970514735\nThank You.'
                subject = 'Hello from RESTO, %s' % form.customername.data
                msg = Message(body=message, subject=subject,
                              sender='restofoodservice@gmail.com', recipients=[form.customeremail.data])
                mail.send(msg)
                db.session.add(reservation1)
                db.session.commit()
                flash('Reservation successfull!!!', category="success")
                return redirect(url_for('index'))
            except:
                flash("Looks like you dont have Internet", category="danger")
        else:
            flash('All Tables are Reserved, Book After a While. ', category="danger")
            return redirect(url_for('reservation'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error during reservation: {err_msg}', category='danger')
        return redirect(url_for('reservation'))
    return render_template('reserve.html', form=form)


@app.route('/restmenu')
def restmenupage():
    dishlist = menu.query.all()
    return render_template('Menu.html', toshowdish=dishlist)


@app.route('/delete/<int:dish_id>')
def delete(dish_id):
    dish_to_delete = menu.query.get_or_404(dish_id)

    try:
        db.session.delete(dish_to_delete)
        db.session.commit()
        flash('Dish Deleted Successfully!!', category="success")
        return redirect(url_for('removedish'))
    except:
        flash('Error Deleting Dish!!', category="danger")
        return redirect(url_for('removedish'))


"""     return render_template('updatedish.html', dish_to_delete=dish_to_delete)
 """


@app.route('/update/<int:dish_id>', methods=['POST', 'GET'])
def update(dish_id):
    form = updatedishForm()
    menu1 = menu.query.all()
    dish_to_update = menu.query.get_or_404(dish_id)

    if request.method == 'POST':
        dish_to_update.dish_name = form.dishname.data
        dish_to_update.dish_price = form.dishprice.data
        dish_to_update.dish_desc = form.dishdesc.data

        try:
            db.session.commit()
            flash('Dish Updated', category='success')
            return redirect(url_for('removedish'))
        except:
            flash('Error Updating Dish!', category='danger')
            return redirect(url_for('removedish'))

    return render_template('updatedish.html',  dish_to_update=dish_to_update, toshowdish=menu1, form=form)


@app.route('/admin/remove/')
def removedish():
    menu1 = menu.query.all()
    return render_template('removedish.html', toshowdish=menu1)


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/showreserve')
def showreserve():
    reservelist = reserve.query.all()
    return render_template('reservation.html', toshowreserve=reservelist)


@app.route('/showorder')
def showorder():
    orders = order.query.all()
    return render_template('orders.html', showorders=orders)


@app.route('/adminorders')
def adminorders():
    adminorderitems = db.session.query(order,menu,customer).select_from(order).join(menu).join(customer).all()

    return render_template('adminorders.html', adminorderitems=adminorderitems)


""" 
@app.route('/custorders')
def custorders():
    custordersfrom = menu.query.all()
    return render_template('orderland.html', toshowdish=custordersfrom)

 """


@app.route('/menucust', methods=['GET', 'POST'])
def menucust():
    add_dish = AddDishForm()
    pord = placeOrdForm()
    if add_dish.validate_on_submit():
        print(add_dish)
    menutodisplay = menu.query.order_by(menu.dish_price)
    orderitems = db.session.query(order, menu).join(menu).all()
    if pord.validate_on_submit():
        flash('Your Order has been Placed!!', category="success")
        return redirect(url_for('index'))
            

    total = 0
    for o, m in orderitems:
        total = total + (m.dish_price * o.ord_dish_count)
    return render_template('menuforcust.html', total=total, pord=pord, menutodisplay=menutodisplay, orderitems=orderitems, add_dish=add_dish)


# cancelling reservation
@app.route('/cancel/<int:reserve_id>')
def cancel(reserve_id):
    reserve_to_cancel = reserve.query.get_or_404(reserve_id)

    try:
        db.session.delete(reserve_to_cancel)
        db.session.commit()
        flash('Reservation cancelled', category="success")
        return redirect(url_for('showreserve'))
    except:
        flash('Error cancelling Reservation', category="danger")
        return redirect(url_for('showreserve'))


@app.route('/delorder/<int:order_id>')
def delorder(order_id):
    order_to_delete = order.query.get_or_404(order_id)

    try:
        db.session.delete(order_to_delete)
        db.session.commit()
        flash('Dish removed from cart', category="success")
        return redirect(url_for('menucust'))
    except:
        flash('Error removing Dish from cart', category="danger")
        return redirect(url_for('menucust'))


@app.route('/cartadd/<int:dish_id>')
def cartadd(dish_id):
    add_to_cart = menu.query.get_or_404(dish_id)
    last = customer.query.order_by(desc(customer.cust_id)).first()
    placing_order = order(ord_cust_id=last.cust_id,
                          ord_dish_id=dish_id,
                          ord_dish_count=1)
    try:
        db.session.add(placing_order)
        db.session.commit()
        flash('Dish Added to Cart', category="success")
        return redirect(url_for('menucust'))
    except:
        flash('Error Adding Dish to Cart', category="danger")

    return render_template('menuforcust.html', add_to_cart=add_to_cart)


""" 
 """


@app.route('/admindelorder/<int:order_id>')
def admindelorder(order_id):
    order_to_delete = order.query.get_or_404(order_id)

    try:
        db.session.delete(order_to_delete)
        db.session.commit()
        flash('Dish served to customer', category="success")
        return redirect(url_for('adminorders'))
    except:
        flash('Error serving Dish to customer', category="danger")
        return redirect(url_for('adminorders'))


@app.route('/adminteam', methods=['GET', 'POST'])
def adminteam():
    allteam = emp.query.all()
    form = addEmpForm()
    if form.validate_on_submit():
        newemp = emp(
            emp_name=form.empname.data,
            emp_desg=form.empdesg.data,
            emp_phno=form.empphno.data,
            emp_salary=form.empsalary.data,
            emp_address=form.empaddress.data
        )
        try:
            db.session.add(newemp)
            db.session.commit()
            flash('Employee added successfully!', category="success")
            return redirect(url_for('adminteam'))
        except:
            flash('Error Adding Employee', category="danger")
            return redirect(url_for('adminteam'))

    return render_template('adminteam.html', allteam=allteam, form=form)


@app.route('/admindelteam/<int:emp_id>')
def admindelteam(emp_id):
    emp_to_delete = emp.query.get_or_404(emp_id)

    try:
        db.session.delete(emp_to_delete)
        db.session.commit()
        flash('Employee Removed', category="success")
        return redirect(url_for('adminteam'))
    except:
        flash('Error Removing Employee!', category="danger")
        return redirect(url_for('adminteam'))


