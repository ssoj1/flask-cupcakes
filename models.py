"""Models for Cupcake app."""

from typing import Optional
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

DEFAULT_IMAGE = 'https://tinyurl.com/demo-cupcake'

class Cupcake(db.Model):
    """Cupcake."""

    __tablename__ = "cupcakes"

    id =  db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)

    flavor = db.Column(db.Text, 
                        nullable=False)
    
    size = db.Column(db.Text, 
                        nullable = False)

    rating = db.Column(db.Integer, 
                        nullable= False)

    image = db.Column(db.Text, 
                        nullable = False,
                        default = DEFAULT_IMAGE)

    def serialize(self):
        """Serialize to dictionary"""

        return {
            "id": self.id, 
            "flavor": self.flavor,
            "size": self.size, 
            "rating": self.rating,
            "image": self.image,
        }

    # def image_url(self):
    #     """Return an image, either the one provided or the default"""

    #     return self.image or DEFAULT_IMAGE