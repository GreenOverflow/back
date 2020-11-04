from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

app = Flask(__name__)
api = Api(app)


class Commune(Resource):
    def get(self, postalcode):
        return {"postalCode": int(postalcode)}


api.add_resource(Commune, '/commune/<postalcode>/statistics')

if __name__ == '__main__':
    app.run(port='4443')
