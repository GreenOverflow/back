from flask import Flask
from flask_restful import Resource, Api
import data_fetch as dataFetch
import re

app = Flask(__name__)
api = Api(app)


class Commune(Resource):
    def get(self, postalcode):
        prog = re.compile('^[0-9]{5}$')
        if not prog.match(postalcode):
            return {"code": "POSTAL_CODE_NOT_FOUND"}, 404

        int(postalcode)

        try:
            result = dataFetch.to_api(dataFetch.indexes(postalcode))
            if len(result.keys()) == 0:
                return {"code": "POSTAL_CODE_NOT_FOUND"}, 404
            else:
                return result
        except:
            return {"code": "UNKNOWN_SERVER_ERROR"}, 500


api.add_resource(Commune, '/commune/<postalcode>/statistics')

if __name__ == '__main__':
    app.run(port='8080')
