from flask import Flask, render_template, request, jsonify
import json
import os
from game import SnakeGame

app = Flask(__name__)
game = None
SETTINGS_FILE = 'settings.json'

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            # Ensure all required settings exist
            if 'high_score' not in settings:
                settings['high_score'] = 0
            if 'speed' not in settings:
                settings['speed'] = 'normal'
            if 'controls' not in settings:
                settings['controls'] = 'arrows'
            return settings
    return {
        'borders': 'kills',
        'lives': 3,
        'high_score': 0,
        'speed': 'normal',
        'controls': 'arrows'
    }

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

@app.route('/')
def home():
    settings = load_settings()
    return render_template('index.html', settings=settings)

@app.route('/start_game', methods=['POST'])
def start_game():
    global game
    settings = load_settings()
    game = SnakeGame(settings)
    return jsonify({'status': 'success'})

@app.route('/get_game_state', methods=['GET'])
def get_game_state():
    if game:
        state = game.get_state()
        # Update high score if current score is higher
        settings = load_settings()
        if state['score'] > settings['high_score']:
            settings['high_score'] = state['score']
            save_settings(settings)
        state['high_score'] = settings['high_score']
        state['controls'] = settings['controls']
        return jsonify(state)
    return jsonify({'status': 'no_game'})

@app.route('/move', methods=['POST'])
def move():
    if game:
        direction = request.json.get('direction')
        game.move(direction)
        return jsonify(game.get_state())
    return jsonify({'status': 'no_game'})

@app.route('/update_settings', methods=['POST'])
def update_settings():
    settings = request.json
    save_settings(settings)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 