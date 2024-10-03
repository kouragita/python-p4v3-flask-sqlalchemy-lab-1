from flask import Flask, jsonify
from flask_migrate import Migrate

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
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    return jsonify({
        "id": earthquake.id,
        "magnitude": earthquake.magnitude,
        "location": earthquake.location,
        "year": earthquake.year
    })

@app.route('/earthquakes/<int:id>')
def earthquake(id):
    return get_earthquake(id)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if not earthquakes:
        return jsonify({"count": 0, "quakes": []}), 200
    return jsonify({"count": len(earthquakes), "quakes": [{
        "id": earthquake.id,
        "magnitude": earthquake.magnitude,
        "location": earthquake.location,
        "year": earthquake.year
    } for earthquake in earthquakes]})

if __name__ == '__main__':
    app.run(port=5555, debug=True)