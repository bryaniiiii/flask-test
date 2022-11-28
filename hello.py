from flask import Flask, jsonify, make_response, session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from functools import wraps
# import pymysql
# import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x8bXN\xe4i\xc9\xf3\x83\x89\xbb%E'
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:AJBNv20J9oGK8o5bk32I@containers-us-west-58.railway.app:7212/railway'
db = SQLAlchemy(app)


class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Video(name = {name}, views = {views}, likes = {likes})"




video_post_args = reqparse.RequestParser()
video_post_args.add_argument("name", type=str, help="Name of the video is required", required=True,location='values')
video_post_args.add_argument("views", type=int, help="Views of the video", required=True,location='values')
video_post_args.add_argument("likes", type=int, help="Likes on the video", required=True,location='values')

video_get_args = reqparse.RequestParser()
video_get_args.add_argument("token", type=str, help="Token is required", required=True,location='headers')

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required",location='values')
video_update_args.add_argument("views", type=int, help="Views of the video",location='values')
video_update_args.add_argument("likes", type=int, help="Likes on the video",location='values')

video_login_args = reqparse.RequestParser()
video_login_args.add_argument("username", type=str, help="Name of the video is required", required=True,location='values')
video_login_args.add_argument("password", type=int, help="Views of the video", required=True,location='values')

resource_fields= {
    'id' : fields.Integer,
    'name' : fields.String,
    'views' : fields.Integer,
    'likes' : fields.Integer
}

def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        args = video_get_args.parse_args()
        token = args['token']
        if not token:
            return jsonify({'Alert!': 'Token is missing!'})

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])

        except:
            return jsonify({'Message': 'Invalid token'})
        return func(*args, **kwargs)
    return decorated

class Video(Resource):
    @token_required
    def get(self, video_id):
        return jsonify({'message': 'Verified'})
        
        # result = VideoModel.query.filter_by(id=video_id).first()
        # if not result:
        #     abort(404, message="could not find video with that id")
        # return result
    
    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_post_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video id already exists")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="video id does not exit")
        
        if args['name']:
            result.name=args['name']
        if args['views']:
            result.views=args['views']
        if args['likes']:
            result.likes=args['likes']


        db.session.commit()
        return result  

class Login(Resource):

    
    def post(self):
        args = video_login_args.parse_args()
        if args['username'] and args['password'] == 123456:
            session['logged_in'] = True

            token = jwt.encode({
                'user': args['username'],
                'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=30)

            }, app.config['SECRET_KEY'],algorithm="HS256"
            )
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'Unable to verify'})



api.add_resource(Video, "/video/<int:video_id>")
api.add_resource(Login, "/login")





if __name__ == "__main__":
    app.run(debug=True)