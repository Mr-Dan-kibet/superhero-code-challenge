from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# error handler
def not_found(resource="Resource"):
    return {"error": f"{resource} not found"}, 404

class Heros(Resource):

    def get(self):
        heroes = Hero.query.all()

        response = [
            {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            }
            for hero in heroes
        ]

        return response, 200

class HeroById(Resource):
    def get(self, id):
        hero = Hero.query.get(id)

        if not hero:
            return {"error": "Hero not found"}, 404

        return {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "hero_powers": [
                {
                    "hero_id": hp.hero_id,
                    "id": hp.id,
                    "power": {
                        "description": hp.power.description,
                        "id": hp.power.id,
                        "name": hp.power.name
                    },
                    "power_id": hp.power_id,
                    "strength": hp.strength
                }
                for hp in hero.hero_powers
            ]
        }, 200


class Powers(Resource):
    def get(self):
        return [
            power.to_dict(only=("description", "id", "name"))
            for power in Power.query.all()
        ], 200



class PowerById(Resource):

    def get(self, id):
        power = Power.query.get(id)

        if not power:
            return not_found("Power")

        response = {
            "description": power.description,
            "id": power.id,
            "name": power.name
        }

        return response, 200
    def patch(self, id):
        power = Power.query.get(id)

        if not power:
            return not_found("Power")

        data = request.get_json()

        if "description" in data:
            if not data["description"]:
                return {"errors": ["Description must be present"]}, 400

            if len(data["description"]) < 20:
                return {"errors": ["Description must be 20 characters or longer"]}, 400

            power.description = data["description"]

        db.session.commit()

        response = {
            "description": power.description,
            "id": power.id,
            "name": power.name
        }

        return response, 200


class HeroPowers(Resource):

    def post(self):
        data = request.get_json()

        try:
            # create HeroPower instance
            hero_power = HeroPower(
                strength=data.get("strength"),
                hero_id=data.get("hero_id"),
                power_id=data.get("power_id")
            )

            db.session.add(hero_power)
            db.session.commit()

            response = {
                "id": hero_power.id,
                "hero_id": hero_power.hero_id,
                "power_id": hero_power.power_id,
                "strength": hero_power.strength,
                "hero": {
                    "id": hero_power.hero.id,
                    "name": hero_power.hero.name,
                    "super_name": hero_power.hero.super_name
                },
                "power": {
                    "id": hero_power.power.id,
                    "name": hero_power.power.name,
                    "description": hero_power.power.description
                }
            }

            return response, 201

        except ValueError as e:
            # catches model validations (strength, etc.)
            return {"errors": [str(e)]}, 400

        except Exception:
            # catches FK errors, missing fields, etc.
            db.session.rollback()
            return {"errors": ["validation errors"]}, 400    


api.add_resource(Heros, "/heroes")
api.add_resource(HeroById, "/heroes/<int:id>")
api.add_resource(Powers, "/powers")
api.add_resource(PowerById, "/powers/<int:id>")
api.add_resource(HeroPowers, "/hero_powers")

if __name__ == '__main__':
    app.run(port=5555, debug=True)