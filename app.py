import random
import marshmallow
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json
from flask_marshmallow import Marshmallow
from flask import Response
from flask import request
from flask_bcrypt import Bcrypt
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Gek313nkL@localhost:3306/lab_py'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

bad_request = "{\"code\": 400,\"message\":\"Invalid request\"}"


class UserSchema(marshmallow.Schema):
    class Meta:
        fields = ('user_id', 'user_name', 'user_email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class PlaylistSchema(marshmallow.Schema):
    class Meta:
        fields = ('playlist_id', 'playlist_name', 'user_id', 'is_private')


playlist_schema = PlaylistSchema()
playlists_schema = PlaylistSchema(many=True)


class MusicSchema(marshmallow.Schema):
    class Meta:
        fields = ('music_id', 'music_name', 'playlist_id')


music_schema = MusicSchema()
musics_schema = MusicSchema(many=True)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    user_password = db.Column(db.String(255))
    user_email = db.Column(db.String(255))
    playlists = db.relationship('Playlist', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.user_name}', '{self.user_email}', '{self.user_id}')"


class Playlist(db.Model):
    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    is_private = db.Column(db.Boolean)
    musics = db.relationship('Music', backref='playlist', lazy=True)

    def __repr__(self):
        return f"Playlist('{self.playlist_name}', '{self.is_private}', '{self.playlist_id}')"


class Music(db.Model):
    music_id = db.Column(db.Integer, primary_key=True)
    music_name = db.Column(db.String(255))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.playlist_id'))

    def __repr__(self):
        return f"Playlist('{self.playlist_name}', '{self.is_private}', '{self.playlist_id}')"


@app.route('/hello-world-9')
def hello_world():
    return 'Hello World 9'


@app.route('/user', methods=['GET'])
def get_users():
    return jsonify(users_schema.dump(User.query.all()))


@app.route('/playlist', methods=['GET'])
def get_playlist():
    return jsonify(playlists_schema.dump(Playlist.query.all()))


@app.route('/music', methods=['GET'])
def get_music():
    return jsonify(musics_schema.dump(Music.query.all()))


@app.route('/user', methods=['POST', 'PUT'])
def add_user():
    body = request.json
    try:
        name = body['user_name']
        password = bcrypt.generate_password_hash(body['user_password'])
        email = body['user_email']
    except KeyError:
        return bad_request, 400
    # PUT
    if request.method == 'PUT':
        try:
            user = User.query.filter_by(user_name=name).first()
            user.user_password = password
            user.user_email = email
            db.session.commit()
        except Exception:
            db.session.rollback()
            return bad_request, 400
        return jsonify(user_schema.dump(user))
    # POST
    if db.session.query(User.user_name).filter_by(user_name=name).first() is not None:
        return bad_request, 400
    user = User(user_name=name, user_password=password, user_email=email, user_id=random.randint(0, 1000000))
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))


@app.route('/playlist', methods=['POST', 'PUT'])
def add_playlist():
    body = request.json
    try:
        name = body['playlist_name']
        is_private = body['is_private']
        user_id = body['user_id']
    except KeyError:
        return bad_request, 400
    # PUT
    if request.method == 'PUT':
        try:
            playlist_id = body['playlist_id']
            playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
            playlist.playlist_name = name
            playlist.user_id = user_id
            playlist.is_private = is_private
            db.session.commit()
        except Exception:
            db.session.rollback()
            return bad_request, 400
        return jsonify(playlist_schema.dump(playlist))
    # POST
    try:
        playlist = Playlist(playlist_id=random.randint(0, 1000000), playlist_name=name, user_id=user_id,
                            is_private=is_private)
        db.session.add(playlist)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return bad_request, 400
    return jsonify(playlist_schema.dump(playlist))


@app.route('/music', methods=['POST', 'PUT'])
def add_music():
    body = request.json
    try:
        name = body['music_name']
        playlist_id = body['playlist_id']
    except KeyError:
        return bad_request, 400
        # PUT
    if request.method == 'PUT':
        try:
            music_id = body['music_id']
            music = Music.query.filter_by(music_id=music_id).first()
            music.music_name = name
            music.playlist_id = playlist_id
            db.session.commit()
        except Exception:
            db.session.rollback()
            return bad_request, 400
        return jsonify(music_schema.dump(music))
    # POST
    try:
        music = Music(music_id=random.randint(0, 1000000), music_name=name, playlist_id=playlist_id)
        db.session.add(music)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return bad_request, 400
    return jsonify(music_schema.dump(music))


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        User.query.filter_by(user_id=user_id).delete()
        db.session.commit()
    except Exception:
        db.session.rollback()
        return bad_request, 400
    return ""


@app.route('/playlist/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    try:
        Playlist.query.filter_by(playlist_id=playlist_id).delete()
        db.session.commit()
    except Exception:
        db.session.rollback()
        return bad_request, 400
    return ""


@app.route('/music/<music_id>', methods=['DELETE'])
def delete_music(music_id):
    try:
        Music.query.filter_by(music_id=music_id).delete()
        db.session.commit()
    except Exception:
        db.session.rollback()
        return bad_request, 400
    return ""


if __name__ == '__main__':
    app.run()
