from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app) 


class Signup (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email



class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Creat a new user
@app.route("/signup", methods=["POST"])
def add_user():
    username = request.json['username']
    password= request.json['password']
    email = request.json['email']
    if Signup.query.filter_by(username = username).first() is not None:
        return jsonify({ 'User already exits': username }), 400# existing user
    new_user = Signup(username, password, email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'User Added':username}) 

@app.route("/user", methods=["GET"])
def get_user():
    all_users = Signup.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route("/login", methods=["POST"])
def user_detail():
    username = request.json['username']
    password= request.json['password']
    if Signup.query.filter_by(username = username).first() is not None:
         return jsonify({ 'Successfully Login': username }), 200
    elif Signup.query.filter_by(username = username).first() is None:
      return jsonify({ 'Sorry can’t find this user, Please Sign Up first.': username }), 400

if __name__ == '__main__':
    app.run(debug=True)