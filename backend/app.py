from flask import Flask, jsonify, redirect, url_for, request
from flask_cors import CORS
from flask_restful import Resource, Api
from google.auth import jwt

from utils import get_comments, eval_sentiment
from database import session, Video, User

app = Flask("Commentary")
cors = CORS(app)
api = Api(app)


class SentimentAnalysis(Resource):
    def delete(self, id, no_of_results=None):
        session.query(Video).delete(Video.video_id == id)
        session.commit()

    def get(self, id, no_of_results=None):
        fetch_all = no_of_results == "all"
        comments = get_comments(id, no_of_results, fetch_all)

        sentiment = eval_sentiment(comments)
        comments_with_sentiment = sentiment["comments"]
        ratio = sentiment["ratio"]
        response = {"ratio": ratio, "comments": comments_with_sentiment}
        video = Video(id, response, len(comments_with_sentiment))
        session.add(video)
        session.commit()

        return jsonify(response)

    def put(self, id, no_of_results=None):
        pass


class Youtube(Resource):
    def get(self, id, no_of_results):
        fetch_all = no_of_results == "all"

        instance = session.query(Video).filter_by(video_id=id).first()
        if instance is not None:
            instance = instance.__dict__
            comments = get_comments(id, no_of_results, fetch_all)
            no_of_new_comments = len(comments) - instance["no_of_comments"]
            response = {
                "ratio": instance["sentiment"]["ratio"],
                "comments": instance["sentiment"]["comments"],
                "is_cached": True,
                "no_of_new_comments": no_of_new_comments,
            }
            return jsonify(response)
        return redirect(
            url_for("sentimentanalysis", id=id, no_of_results=no_of_results)
        )


class Google(Resource):
    def post(self):
        token = request.json.get("credential")

        claims = jwt.decode(token, verify=False)
        email = claims.get("email")
        name = claims.get("name")
        sub = claims.get("sub")
        picture = claims.get("picture")

        instance = session.query(User).filter_by(uuid=sub).first()
        if instance:
            return jsonify(
                {
                    "name": instance.name,
                    "email": instance.email,
                    "picture": instance.picture,
                }
            )

        user = User(sub, name, email, picture)
        session.add(user)
        session.commit()
        return jsonify({"email": email, "name": name, "picture": picture})


api.add_resource(SentimentAnalysis, "/analysis/<id>/<no_of_results>")
api.add_resource(Youtube, "/youtube/<id>/<no_of_results>")
api.add_resource(Google, "/google")

if __name__ == "__main__":
    app.run(debug=True, port=5003)
