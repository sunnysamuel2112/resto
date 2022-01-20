
from flask_mail import Mail,Message
from resto import app  # goto inint
#mailapp
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'restofoodservice@gmail.com'
app.config['MAIL_PASSWORD'] = 'resto@2000'

mail = Mail(app)




if __name__ == '__main__':
    app.run(debug=True)
