import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# POSTGRES_USER = postgres
# POSTGRES_PW = password
# POSTGRES_URL = AWS RDS Endpoint
# POSTGRES_DB = name of db in pgdmin

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:' +
    f'{os.getenv("POSTGRES_PW")}@{os.getenv("POSTGRES_URL")}/{os.getenv("POSTGRES_DB")}'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    amount = db.Column(db.Float)

    def __init__(self, first_name: str, last_name: str, amount: float):
        self.first_name = first_name
        self.last_name = last_name
        self.amount = amount

    def __repr__(self):
        return f'{self.first_name} {self.last_name} spent {self.amount}'


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/list_db')
def list_db():
    transactions = Transaction.query.all()
    return '\n'.join([str(transaction) for transaction in transactions])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
