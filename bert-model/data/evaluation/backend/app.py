from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/<sentiment>', methods=["POST"])
def hello(sentiment):
    text = request.json
    with open(f'../../evaluated/{sentiment}.txt', 'a') as f:
        f.write(text + '\n')
    return "hello"


if __name__ == "__main__":
    app.run(debug=True, port=8080)
    