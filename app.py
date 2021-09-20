"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request
# from flask_debugtoolbar import DebugToolbarExtension
from models import Cupcake, db, connect_db

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get("/api/cupcakes")
def list_all_cupcakes():
    """Return a list of all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.get("/api/cupcakes/<int:cupcake_id>")
def return_cupcake_detail(cupcake_id):
    """ Returns a dictionary of cupcake information """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post("/api/cupcakes")
def create_cupcake():
    """ Creates a new cupcake and respond with JSON like: 
    {cupcake: {id, flavor, size, rating, image}}. 
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(
        flavor=flavor, 
        size=size, 
        rating=rating, 
        image=image)
    
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized),201)


