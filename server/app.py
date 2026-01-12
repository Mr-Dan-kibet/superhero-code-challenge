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
        return [hero.to_dict() for hero in Hero.query.all()], 200

class HeroById(Resource):

    def get(self, id):
        hero = Hero.query.get(id)

        if not hero:
            return not_found("Hero")

        return hero.to_dict(), 200

class Powers(Resource):
    def get(self):
        return [power.to_dict() for power in Power.query.all()], 200


class PowerById(Resource):

    def get(self, id):
        power = Power.query.get(id)

        if not power:

            return not_found("Power")

        return power.to_dict(), 200


api.add_resource(Heros, "/heros")
api.add_resource(HeroById, "/heros/<int:id>")
api.add_resource(Powers, "/powers")




if __name__ == '__main__':
    app.run(port=5555, debug=True)