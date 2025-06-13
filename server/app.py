from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db=SQLAlchemy()
migrate= Migrate()

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)
migrate.init_app(app,db)


if __name__ == '__main__':
    app.run(port=5555, debug=True)