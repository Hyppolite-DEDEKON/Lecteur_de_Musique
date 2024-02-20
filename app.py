from flask import Flask, render_template
from flask_socketio import SocketIO
import os
from pygame import mixer
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

mixer.init()
playing = False
playlist = []
current_track = 0

def play_music():
    global playing
    while True:
        if playing and not mixer.music.get_busy():
            next_track()
        socketio.sleep(1)

def next_track():
    global current_track
    if playlist:
        current_track = (current_track + 1) % len(playlist)
        play_track()

def play_track():
    global playing
    if playlist:
        mixer.music.load(playlist[current_track])
        mixer.music.play()
        playing = True

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('play_pause')
def play_pause():
    global playing
    playing = not playing
    if playing:
        play_track()

@socketio.on('next_track')
def next_track_socket():
    next_track()

@socketio.on('add_track')
def add_track(data):
    playlist.append(data['file'])
    if not playing:
        play_track()

if __name__ == '__main__':
    # Utilisez cette section pour exécuter localement
    socketio.start_background_task(play_music)
    socketio.run(app, debug=True)

    # Utilisez cette section pour déployer sur un serveur
    # socketio.start_background_task(play_music)
    # socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
