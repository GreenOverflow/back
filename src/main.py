from flask import Flask, send_file
from flask_restful import Resource, Api
from src import data_fetch as dataFetch
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


class CommunePdf(Resource):
    def get(self, postalcode):
        prog = re.compile('^[0-9]{5}$')
        if not prog.match(postalcode):
            return {"code": "POSTAL_CODE_NOT_FOUND"}, 404

        int(postalcode)

        #test l'existance du pdf
        #if absent generer le pdf

        try:
            return send_file('./report/{}_stat_report.pdf'.format(postalcode), attachment_filename='{}_stat_report.pdf'.format(postalcode))
        except Exception as e:
            return str(e)


api.add_resource(Commune, '/commune/<postalcode>/statistics')
api.add_resource(CommunePdf, '/commune/<postalcode>/stat_report.pdf')

if __name__ == '__main__':
    app.run(port='8080')
