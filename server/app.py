from flask import Flask, make_response
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquake')
def list_eartquakes():
    all_earthis = Earthquake.query.all()
    Earthquake_list = [earthie.to_dict() for earthie in all_earthis]
    resp_body = Earthquake_list
    resp_code = 200
    return make_response(resp_body, resp_code)
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)