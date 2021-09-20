from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

CUPCAKE_UPDATE_DATA = {
    "flavor": "Banana"
}

CUPCAKE_UPDATE_DATA_2 = {
    "flavor": "Cherry",
    "size": "large",
    "rating": 6,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        # self.cupcake = cupcake
        self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake_id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            copy_data = resp.json.copy()
            del copy_data['cupcake']['id']

            self.assertEqual(copy_data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """ Tests that if you change one or many fields
            will update database correctly
        """
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            # breakpoint()
            resp = client.patch(url, json=CUPCAKE_UPDATE_DATA)
            # breakpoint()
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            copy_data = resp.json.copy()
            del copy_data['cupcake']['id']
            breakpoint()
            self.assertEqual(copy_data, { "cupcake" : {
                "flavor": "Banana",
                "size": "TestSize",
                "rating": 5,
                "image": "http://test.com/cupcake.jpg"}
                })

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.patch(url, json=CUPCAKE_UPDATE_DATA_2)

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            copy_data = resp.json.copy()
            del copy_data['cupcake']['id']

            self.assertEqual(copy_data, { "cupcake": {
                "flavor": "Cherry",
                "size": "large",
                "rating": 6,
                "image": "http://test.com/cupcake2.jpg"}
            })