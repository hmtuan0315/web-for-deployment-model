from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request, jsonify

app = Flask(__name__)
cors = CORS(app, headers=['Content-Type'], expose_headers=['Access-Control-Allow-Origin'], supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'


# text_input = ["it's a bad movie out of the time", "you're a murder, but you still have morality"]

@app.route('api/cls_lstm/', methods=['POST'], strict_slashes=False)
def classification():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True)
