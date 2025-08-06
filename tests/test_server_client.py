"""
Tests for the server/client Wordle game mode.

This module contains unit tests for the server/client architecture.
"""

import pytest
import time
import threading
from unittest.mock import patch, MagicMock
from src.game_modes.server_client import ServerGame, ClientGame
from src.game_modes.single_player import SinglePlayerGame
from src.game_modes.cheating_host import CheatingHostGame


class TestServerGame:
    """Test cases for the ServerGame class."""
    
    def test_server_initialization(self):
        """Test that a server can be initialized correctly."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        server = ServerGame(word_list, max_rounds=6, port=5000)
        
        assert server.port == 5000
        assert server.word_list == word_list
        assert server.max_rounds == 6
        assert len(server.active_games) == 0
    
    def test_server_has_flask_app(self):
        """Test that the server has a Flask app."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        server = ServerGame(word_list, max_rounds=6, port=5000)
        
        assert hasattr(server, 'app')
        assert server.app is not None
    
    def test_server_has_routes(self):
        """Test that the server has the expected routes."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        server = ServerGame(word_list, max_rounds=6, port=5000)
        
        # Check that routes are registered
        routes = [rule.rule for rule in server.app.url_map.iter_rules()]
        
        assert '/api/game/start' in routes
        assert '/api/game/guess' in routes
        assert '/api/game/state/<session_id>' in routes
        assert '/api/game/reset/<session_id>' in routes
        assert '/api/health' in routes


class TestClientGame:
    """Test cases for the ClientGame class."""
    
    def test_client_initialization(self):
        """Test that a client can be initialized correctly."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        client = ClientGame(word_list, max_rounds=6, server_url='http://localhost:5000')
        
        assert client.server_url == 'http://localhost:5000'
        assert client.word_list == word_list
        assert client.max_rounds == 6
        assert client.session_id is None
    
    def test_client_initial_game_state(self):
        """Test that the client has the correct initial game state."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        client = ClientGame(word_list, max_rounds=6, server_url='http://localhost:5000')
        
        state = client.game_state
        assert state['game_state'] == 'waiting'
        assert state['current_round'] == 0
        assert state['max_rounds'] == 6
        assert state['remaining_rounds'] == 6
        assert state['is_game_over'] is False
    
    @patch('src.game_modes.server_client.requests.get')
    def test_client_make_request_get(self, mock_get):
        """Test that the client can make GET requests."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        client = ClientGame(word_list, max_rounds=6, server_url='http://localhost:5000')
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'success'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = client._make_request('/api/health', 'GET')
        
        assert result == {'status': 'success'}
        mock_get.assert_called_once_with('http://localhost:5000/api/health')
    
    @patch('src.game_modes.server_client.requests.post')
    def test_client_make_request_post(self, mock_post):
        """Test that the client can make POST requests."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        client = ClientGame(word_list, max_rounds=6, server_url='http://localhost:5000')
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'success'}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        data = {'test': 'data'}
        result = client._make_request('/api/test', 'POST', data)
        
        assert result == {'status': 'success'}
        mock_post.assert_called_once_with('http://localhost:5000/api/test', json=data)
    
    @patch('src.game_modes.server_client.requests.post')
    def test_client_start_game(self, mock_post):
        """Test that the client can start a game."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        client = ClientGame(word_list, max_rounds=6, server_url='http://localhost:5000')
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'session_id': 'test_session',
            'game_state': {
                'game_state': 'playing',
                'current_round': 0,
                'max_rounds': 6
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        client.start_game(mode='single')
        
        assert client.session_id == 'test_session'
        assert client.game_state['game_state'] == 'playing'
    
    @patch('src.game_modes.server_client.requests.post')
    def test_client_make_guess(self, mock_post):
        """Test that the client can make a guess."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        client = ClientGame(word_list, max_rounds=6, server_url='http://localhost:5000')
        client.session_id = 'test_session'
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': {
                'success': True,
                'result': ['hit', 'miss', 'miss', 'miss', 'miss'],
                'is_correct': False
            },
            'game_state': {
                'game_state': 'playing',
                'current_round': 1
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = client.make_guess('HELLO')
        
        assert result['success'] is True
        assert result['result'] == ['hit', 'miss', 'miss', 'miss', 'miss']
        assert result['is_correct'] is False


class TestServerClientIntegration:
    """Integration tests for server/client communication."""
    
    def test_server_client_communication(self):
        """Test basic server/client communication."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        
        # Create server and client
        server = ServerGame(word_list, max_rounds=6, port=5001)
        client = ClientGame(word_list, max_rounds=6, server_url='http://localhost:5001')
        
        # Test that server and client can be created
        assert server is not None
        assert client is not None
    
    @patch('src.game_modes.server_client.requests.get')
    def test_client_handles_server_error(self, mock_get):
        """Test that client handles server errors gracefully."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        client = ClientGame(word_list, max_rounds=6, server_url='http://localhost:5000')
        client.session_id = 'test_session'
        
        # Mock server error
        mock_get.side_effect = Exception("Connection failed")
        
        # Should return cached state when server is unavailable
        state = client.get_game_state()
        assert state == client.game_state


if __name__ == '__main__':
    pytest.main([__file__]) 