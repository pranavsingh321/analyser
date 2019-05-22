# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

# bow_transformer = CountVectorizer(analyzer=text_process).fit(X)

# def compose(*funcs):
#     return lambda x: reduce(lambda f, g: g(f), list(funcs), x)

# p = compose(foo1, foo2, foo3)
# res = p(range(0, 5))

from flask import Blueprint, jsonify, request
from app import app, db
from models import CampaignAnalysis


api = Blueprint('api', __name__)

INTERNAL_SERVER_ERROR_MESSAGE = {'message': 'An internal error occurred.'}
BAD_REQUEST_MESSAGE = {'message': 'Bad request.'}
OK_MESSAGE = {'message': 'Operation successful.'}


@api.route('/v1/reviews', methods=['POST'])
def receive_reviews():
    reviews = request.form.get('reviews')
    rating = request.form.get('rating')
    language = request.form.get('language')
    if not reviews or not rating or not language:
        return jsonify(BAD_REQUEST_MESSAGE), 400
    else:
        try:
            ReviewsReader.parse(reviews, rating, language)
            return jsonify(OK_MESSAGE), 200

@api.route('/v1/result', methods=['GET'])
def receive_reviews():
    reviews = request.form.get('reviews')
    rating = request.form.get('rating')
    if not reviews or not rating:
        return jsonify(BAD_REQUEST_MESSAGE), 400
    else:
        try:
            db.session.query(Analysis).all()
            return jsonify(OK_MESSAGE), 200
        except IntegrityError:
            return jsonify(BAD_REQUEST_MESSAGE), 400
