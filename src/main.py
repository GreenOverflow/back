from flask import Flask, send_file
from flask_restful import Resource, Api
from data_fetch import to_api, indexes
from pdf_generator import generate_pdf
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
            result = to_api(indexes(postalcode))
            if result is None:
                return {"code": "POSTAL_CODE_NOT_FOUND"}, 404
            else:
                return result
        except Exception:
            return {"code": "UNKNOWN_SERVER_ERROR"}, 500


class CommunePdf(Resource):
    def get(self, postalcode):
        prog = re.compile('^[0-9]{5}$')
        if not prog.match(postalcode):
            return {"code": "POSTAL_CODE_NOT_FOUND"}, 404

        generate_pdf(postalcode)

        try:
            return send_file(f"./report/{postalcode}_stat_report.pdf", attachment_filename=f"{postalcode}_stat_report.pdf")
        except Exception as e:
            return str(e)


api.add_resource(Commune, '/commune/<postalcode>/statistics')
api.add_resource(CommunePdf, '/commune/<postalcode>/stat_report.pdf')

if __name__ == '__main__':
    app.run(port='8080')
