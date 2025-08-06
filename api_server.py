#!/usr/bin/env python3
"""
Simple Flask API server for the Wordle game.

This server provides REST API endpoints for the web interface to communicate with.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Change to src directory and add to path
os.chdir(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.getcwd())

from game_modes.single_player import SinglePlayerGame
from game_modes.cheating_host import CheatingHostGame
from utils.word_loader import get_default_word_list

app = Flask(__name__)
CORS(app)

# Global game instances
games = {}

@app.route('/api/game/start', methods=['POST'])
def start_game():
    """Start a new game."""
    try:
        data = request.get_json() or {}
        game_mode = data.get('mode', 'single')
        session_id = data.get('session_id', f'session_{len(games)}')
        
        # Load word list
        word_list = get_default_word_list()
        
        # Create game based on mode
        if game_mode == 'single':
            game = SinglePlayerGame(word_list, max_rounds=6)
        elif game_mode == 'cheating':
            game = CheatingHostGame(word_list, max_rounds=6)
        else:
            return jsonify({'error': 'Invalid game mode'}), 400
        
        # Start the game
        game.start_game()
        
        # Store the game
        games[session_id] = {
            'game': game,
            'mode': game_mode
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'game_state': game.get_game_state()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/game/guess', methods=['POST'])
def make_guess():
    """Make a guess in the game."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        session_id = data.get('session_id')
        guess = data.get('guess')
        
        if not session_id or not guess:
            return jsonify({'error': 'Missing session_id or guess'}), 400
        
        if session_id not in games:
            return jsonify({'error': 'Game not found'}), 404
        
        game = games[session_id]['game']
        result = game.make_guess(guess)
        
        return jsonify({
            'success': True,
            'result': result,
            'game_state': game.get_game_state()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/game/state/<session_id>', methods=['GET'])
def get_game_state(session_id):
    """Get the current game state."""
    try:
        if session_id not in games:
            return jsonify({'error': 'Game not found'}), 404
        
        game = games[session_id]['game']
        return jsonify(game.get_game_state())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/game/reset/<session_id>', methods=['POST'])
def reset_game(session_id):
    """Reset a game."""
    try:
        if session_id not in games:
            return jsonify({'error': 'Game not found'}), 404
        
        game = games[session_id]['game']
        game.start_game()
        
        return jsonify({
            'success': True,
            'game_state': game.get_game_state()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'active_games': len(games)
    })

if __name__ == '__main__':
    print("🚀 Starting Wordle API Server on http://localhost:5001")
    print("📊 API endpoints:")
    print("   POST /api/game/start - Start a new game")
    print("   POST /api/game/guess - Make a guess")
    print("   GET  /api/game/state/<session_id> - Get game state")
    print("   POST /api/game/reset/<session_id> - Reset game")
    print("   GET  /api/health - Health check")
    
    app.run(host='0.0.0.0', port=5001, debug=True) 