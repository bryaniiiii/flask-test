from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import pymysql
import psycopg2

app = Flask(__name__)
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

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True,location='values')
video_put_args.add_argument("views", type=int, help="Views of the video", required=True,location='values')
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True,location='values')

resource_fields= {
    'id' : fields.Integer,
    'name' : fields.String,
    'views' : fields.Integer,
    'likes' : fields.Integer
}
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required",location='values')
video_update_args.add_argument("views", type=int, help="Views of the video",location='values')
video_update_args.add_argument("likes", type=int, help="Likes on the video",location='values')

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="could not find video with that id")
        return result
    
    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_put_args.parse_args()
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

api.add_resource(Video, "/video/<int:video_id>")





if __name__ == "__main__":
    app.run(debug=True)