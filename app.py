from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Gek313nkL@localhost:3306/lab_py'
db = SQLAlchemy(app)


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


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    user = User(user_id=3, user_name='name', user_password='pass', user_email='email')
    db.session.add(user)
    db.session.commit()
    return "got user"


@app.route('/add_playlist', methods=['GET', 'POST'])
def add_playlist():
    playlist = Playlist(playlist_id=3, playlist_name=None, user_id=None, is_private=None)
    db.session.add(playlist)
    db.session.commit()
    return "got playlist"


@app.route('/add_music', methods=['GET', 'POST'])
def add_music():
    music = Music(music_id=3, music_name=None, playlist_id=None)
    db.session.add(music)
    db.session.commit()
    return "got music"


if __name__ == '__main__':
    app.run()
