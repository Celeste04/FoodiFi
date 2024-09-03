from flask import Flask, jsonify, send_file
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
import product_prices
import tts

app = Flask(__name__)
CORS(app)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('text', type=str, help='text for tts to read out.')

class ProductPrice(Resource):
    def get(self, product_name):
        if product_name == "":
            return jsonify({'error': 'Product name is missing'}), 400
        else:
            n, p = product_prices.get_lowest_price(product_name)
            return jsonify({n : p}), 200

class FrogTTS(Resource):
    def post(self):
        args = parser.parse_args(strict=True)
        if not args['text']:
            return jsonify({'error': 'text is missing'}), 400
        file_path = tts.get_tts(args['text'])
        return send_file(file_path, mimetype="audio/wav", as_attachment=True), 201


        
api.add_resource(ProductPrice, '/products/<product_name>')
api.add_resource(FrogTTS, '/tts')

if __name__ == '__main__':
    app.run(debug=True)