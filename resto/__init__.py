from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SECRET_KEY'] = '7911449938800f82bc6a03af'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

#if __name__ == '__main__':
    #manager.run()

from resto import routes


