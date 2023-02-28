import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api
import utils

app = Flask("Analiza Sentymentu")
cors = CORS(app)
api = Api(app)


class SentimentAnalysis(Resource):
    def post(self):
        sentiment = {}
        body = request.json

        if "content" not in body:
            return {"message": "Key 'content' is missing in body."}, 406

        content = body["content"]
        ratio = {}
        if type(content) is list:
            sentiment = utils.eval_sentiment_list(content)
            ratio = self.get_ratio(sentiment).to_dict()
        else:
            sentiment = utils.eval_sentiment(content)
            ratio = self.get_ratio([sentiment]).to_dict()

        response = jsonify({"ratio": ratio, "comments": sentiment})
        return response

    def get_ratio(self, sentiment):
        df = pd.DataFrame(sentiment)
        return df["sentiment"].value_counts(normalize=True).mul(100).round(1)


api.add_resource(SentimentAnalysis, "/api/sentiment-analysis")

if __name__ == "__main__":
    app.run(debug=True, port=5002)
