#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():
    games = [game.to_dict() for game in Game.query.all()]
    return jsonify(games), 200

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter_by(id=id).first()

    if game:
        game_dict = game.to_dict()
        return jsonify(game_dict), 200
    else:
        response_body = {"message": "Game not found"}
        return jsonify(response_body), 404

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        reviews = [review.to_dict() for review in Review.query.all()]
        return jsonify(reviews), 200
    elif request.method == 'POST':
        new_review = Review(
            score=request.form.get("score"),
            comment=request.form.get("comment"),
            game_id=request.form.get("game_id"),
            user_id=request.form.get("user_id"),
        )

        db.session.add(new_review)
        db.session.commit()

        review_dict = new_review.to_dict()

        return jsonify(review_dict), 201

@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    review = Review.query.filter_by(id=id).first()

    if review is None:
        response_body = {"message": "Review not found"}
        return jsonify(response_body), 404

    if request.method == 'GET':
        review_dict = review.to_dict()
        return jsonify(review_dict), 200
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(review, attr, request.form.get(attr))

        db.session.add(review)
        db.session.commit()

        review_dict = review.to_dict()
        return jsonify(review_dict), 200
    elif request.method == 'DELETE':
        db.session.delete(review)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."
        }

        return jsonify(response_body), 200

@app.route('/users')
def users():
    users = [user.to_dict() for user in User.query.all()]
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(port=5555)
