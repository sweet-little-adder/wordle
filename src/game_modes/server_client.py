"""
Server/Client Wordle game mode.

This module implements the server/client architecture for Task 2.
The server manages the game state and clients connect to play.
"""

import json
import threading
import time
from typing import List, Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
from .base_game_mode import BaseGameMode
from ..core.game_engine import WordleGame, GameState


class ServerGame(BaseGameMode):
    """
    Server-side game implementation for server/client mode.
    
    This class manages the game state on the server side and provides
    REST API endpoints for clients to interact with.
    """
    
    def __init__(self, word_list: List[str], max_rounds: int = 6, port: int = 5000):
        """
        Initialize the server game.
        
        Args:
            word_list: List of valid 5-letter words
            max_rounds: Maximum number of guessing rounds
            port: Port to run the server on
        """
        super().__init__(word_list, max_rounds)
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for web clients
        self.active_games = {}  # Store active games by session ID
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up Flask routes for the API."""
        
        @self.app.route('/api/game/start', methods=['POST'])
        def start_game():
            """Start a new game."""
            try:
                data = request.get_json() or {}
                session_id = data.get('session_id', f'session_{int(time.time())}')
                game_mode = data.get('mode', 'single')
                
                # Create new game
                if game_mode == 'single':
                    game = SinglePlayerGame(self.word_list, self.max_rounds)
                    game.start_game()
                elif game_mode == 'cheating':
                    game = CheatingHostGame(self.word_list, self.max_rounds)
                    game.start_game()
                else:
                    return jsonify({'error': 'Invalid game mode'}), 400
                
                self.active_games[session_id] = game
                
                return jsonify({
                    'session_id': session_id,
                    'game_state': game.get_game_state(),
                    'message': 'Game started successfully'
                })
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/game/guess', methods=['POST'])
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
                
                if session_id not in self.active_games:
                    return jsonify({'error': 'Game not found'}), 404
                
                game = self.active_games[session_id]
                result = game.make_guess(guess)
                
                return jsonify({
                    'result': result,
                    'game_state': game.get_game_state()
                })
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/game/state/<session_id>', methods=['GET'])
        def get_game_state(session_id):
            """Get the current game state."""
            try:
                if session_id not in self.active_games:
                    return jsonify({'error': 'Game not found'}), 404
                
                game = self.active_games[session_id]
                return jsonify(game.get_game_state())
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/game/reset/<session_id>', methods=['POST'])
        def reset_game(session_id):
            """Reset a game."""
            try:
                if session_id not in self.active_games:
                    return jsonify({'error': 'Game not found'}), 404
                
                game = self.active_games[session_id]
                game.start_game()
                
                return jsonify({
                    'message': 'Game reset successfully',
                    'game_state': game.get_game_state()
                })
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                'status': 'healthy',
                'active_games': len(self.active_games),
                'timestamp': time.time()
            })
    
    def start_server(self, host: str = '0.0.0.0', debug: bool = False):
        """
        Start the Flask server.
        
        Args:
            host: Host to bind to
            debug: Enable debug mode
        """
        print(f"🚀 Starting Wordle server on {host}:{self.port}")
        print(f"📊 API endpoints:")
        print(f"   POST /api/game/start - Start a new game")
        print(f"   POST /api/game/guess - Make a guess")
        print(f"   GET  /api/game/state/<session_id> - Get game state")
        print(f"   POST /api/game/reset/<session_id> - Reset game")
        print(f"   GET  /api/health - Health check")
        
        self.app.run(host=host, port=self.port, debug=debug)
    
    # Required BaseGameMode methods (not used in server mode)
    def start_game(self, **kwargs):
        """Not used in server mode."""
        pass
    
    def make_guess(self, guess: str, **kwargs):
        """Not used in server mode."""
        pass
    
    def get_game_state(self):
        """Not used in server mode."""
        pass
    
    def is_game_over(self):
        """Not used in server mode."""
        pass
    
    def get_winner(self):
        """Not used in server mode."""
        pass


class ClientGame(BaseGameMode):
    """
    Client-side game implementation for server/client mode.
    
    This class communicates with the server to play the game.
    """
    
    def __init__(self, word_list: List[str], max_rounds: int = 6, server_url: str = 'http://localhost:5000'):
        """
        Initialize the client game.
        
        Args:
            word_list: List of valid 5-letter words (for validation)
            max_rounds: Maximum number of guessing rounds
            server_url: URL of the server
        """
        super().__init__(word_list, max_rounds)
        self.server_url = server_url.rstrip('/')
        self.session_id = None
        self.game_state = {
            'game_state': 'waiting',
            'current_round': 0,
            'max_rounds': max_rounds,
            'remaining_rounds': max_rounds,
            'guesses': [],
            'results': [],
            'answer': None,
            'is_game_over': False
        }
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict:
        """
        Make a request to the server.
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Request data
            
        Returns:
            Response data
        """
        import requests
        
        url = f"{self.server_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                response = requests.post(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Server communication error: {e}")
    
    def start_game(self, mode: str = 'single', session_id: str = None) -> None:
        """
        Start a new game on the server.
        
        Args:
            mode: Game mode ('single' or 'cheating')
            session_id: Optional session ID to reuse
        """
        if session_id:
            self.session_id = session_id
        else:
            self.session_id = f"client_{int(time.time())}"
        
        data = {
            'session_id': self.session_id,
            'mode': mode
        }
        
        response = self._make_request('/api/game/start', 'POST', data)
        
        if 'error' in response:
            raise RuntimeError(f"Failed to start game: {response['error']}")
        
        self.session_id = response['session_id']
        self.game_state = response['game_state']
    
    def make_guess(self, guess: str) -> Dict[str, Any]:
        """
        Make a guess by sending it to the server.
        
        Args:
            guess: The word to guess
            
        Returns:
            Dictionary containing the result of the guess
        """
        if not self.session_id:
            raise RuntimeError("No active game session. Call start_game() first.")
        
        data = {
            'session_id': self.session_id,
            'guess': guess
        }
        
        response = self._make_request('/api/game/guess', 'POST', data)
        
        if 'error' in response:
            return {
                'success': False,
                'error': response['error']
            }
        
        self.game_state = response['game_state']
        return response['result']
    
    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current game state from the server.
        
        Returns:
            Dictionary containing the current game state
        """
        if not self.session_id:
            return self.game_state
        
        try:
            response = self._make_request(f'/api/game/state/{self.session_id}')
            self.game_state = response
            return response
        except Exception as e:
            # Return cached state if server is unavailable
            return self.game_state
    
    def is_game_over(self) -> bool:
        """
        Check if the game is over.
        
        Returns:
            True if the game is over, False otherwise
        """
        return self.game_state.get('is_game_over', False)
    
    def get_winner(self) -> Optional[str]:
        """
        Get the winner of the game.
        
        Returns:
            Winner identifier or None if no winner
        """
        if self.game_state.get('game_state') == 'won':
            return 'Player'
        return None
    
    def reset_game(self) -> None:
        """Reset the game on the server."""
        if not self.session_id:
            raise RuntimeError("No active game session.")
        
        response = self._make_request(f'/api/game/reset/{self.session_id}', 'POST')
        
        if 'error' in response:
            raise RuntimeError(f"Failed to reset game: {response['error']}")
        
        self.game_state = response['game_state']


# Import the game mode classes
from .single_player import SinglePlayerGame
from .cheating_host import CheatingHostGame 