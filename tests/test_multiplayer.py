"""
Tests for the multiplayer Wordle game mode.

This module contains unit tests for the multiplayer game functionality.
"""

import pytest
import time
from src.game_modes.multiplayer import MultiplayerGame
from src.core.game_engine import GameState, LetterResult


class TestMultiplayerGame:
    """Test cases for the MultiplayerGame class."""
    
    def test_multiplayer_initialization(self):
        """Test that a multiplayer game can be initialized correctly."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        assert game.max_rounds == 6
        assert game.max_players == 4
        assert game.word_list == word_list
        assert len(game.players) == 0
        assert game.game_state == GameState.PLAYING
    
    def test_add_player(self):
        """Test that players can be added to the game."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        result = game.add_player('player1', 'Alice')
        
        assert result['success'] is True
        assert 'player1' in game.players
        assert game.players['player1']['name'] == 'Alice'
        assert game.players['player1']['score'] == 0
        assert game.players['player1']['has_won'] is False
    
    def test_add_player_duplicate(self):
        """Test that duplicate players are rejected."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        result = game.add_player('player1', 'Bob')
        
        assert result['success'] is False
        assert 'already in the game' in result['error']
    
    def test_add_player_max_players(self):
        """Test that adding more than max players is rejected."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=2)
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        result = game.add_player('player3', 'Charlie')
        
        assert result['success'] is False
        assert 'full' in result['error']
    
    def test_remove_player(self):
        """Test that players can be removed from the game."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        
        result = game.remove_player('player1')
        
        assert result['success'] is True
        assert 'player1' not in game.players
        assert 'player2' in game.players
    
    def test_remove_player_not_found(self):
        """Test that removing non-existent player is rejected."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        result = game.remove_player('nonexistent')
        
        assert result['success'] is False
        assert 'not found' in result['error']
    
    def test_start_game_insufficient_players(self):
        """Test that game cannot start with insufficient players."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        
        with pytest.raises(ValueError, match="Need at least 2 players"):
            game.start_game()
    
    def test_start_game_success(self):
        """Test that game can start with sufficient players."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        
        game.start_game()
        
        assert game.answer is not None
        assert game.answer in word_list
        assert game.game_state == GameState.PLAYING
        assert game.current_round == 0
    
    def test_make_guess_player_not_found(self):
        """Test that guess from non-existent player is rejected."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        result = game.make_guess('HELLO', 'nonexistent')
        
        assert result['success'] is False
        assert 'not found' in result['error']
    
    def test_make_guess_invalid_word(self):
        """Test that invalid guesses are rejected."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        game.start_game()
        
        result = game.make_guess('INVALID', 'player1')
        
        assert result['success'] is False
        assert 'Invalid guess' in result['error']
    
    def test_make_guess_success(self):
        """Test that valid guesses are processed correctly."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        game.start_game()
        
        # Set a known answer for testing
        game.answer = 'HELLO'
        
        result = game.make_guess('WORLD', 'player1')
        
        assert result['success'] is True
        assert len(result['result']) == 5
        assert result['is_correct'] is False
        assert result['round_score'] >= 0
        assert result['total_score'] >= 0
    
    def test_make_guess_correct_answer(self):
        """Test that correct guesses win the game."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        game.start_game()
        
        # Set a known answer for testing
        game.answer = 'HELLO'
        
        result = game.make_guess('HELLO', 'player1')
        
        assert result['success'] is True
        assert result['is_correct'] is True
        assert game.game_state == GameState.WON
        assert game.players['player1']['has_won'] is True
        assert game.players['player1']['rounds_to_win'] == 1
    
    def test_get_game_state(self):
        """Test that game state is returned correctly."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        game.start_game()
        
        state = game.get_game_state()
        
        assert state['game_state'] == GameState.PLAYING.value
        assert state['current_round'] == 0
        assert state['max_rounds'] == 6
        assert state['remaining_rounds'] == 6
        assert state['player_count'] == 2
        assert state['max_players'] == 4
        assert state['answer'] is None  # Answer should be hidden during play
        assert state['is_game_over'] is False
        assert len(state['players']) == 2
    
    def test_get_player_state(self):
        """Test that player state is returned correctly."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        game.start_game()
        
        player_state = game.get_player_state('player1')
        
        assert player_state['player_id'] == 'player1'
        assert player_state['player_name'] == 'Alice'
        assert player_state['score'] == 0
        assert player_state['has_won'] is False
        assert len(player_state['guesses']) == 0
        assert len(player_state['results']) == 0
    
    def test_get_leaderboard(self):
        """Test that leaderboard is calculated correctly."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        game.start_game()
        
        # Set a known answer and make some guesses
        game.answer = 'HELLO'
        game.make_guess('WORLD', 'player1')  # Should get some points
        game.make_guess('PYTHON', 'player2')  # Should get some points
        
        leaderboard = game.get_leaderboard()
        
        assert len(leaderboard) == 2
        assert leaderboard[0]['rank'] == 1
        assert leaderboard[1]['rank'] == 2
        assert all('player_id' in entry for entry in leaderboard)
        assert all('player_name' in entry for entry in leaderboard)
        assert all('score' in entry for entry in leaderboard)
    
    def test_is_game_over(self):
        """Test that game over state is detected correctly."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        # Game should not be over initially
        assert game.is_game_over() is False
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        game.start_game()
        
        # Game should not be over after starting
        assert game.is_game_over() is False
        
        # Make a correct guess to end the game
        game.answer = 'HELLO'
        game.make_guess('HELLO', 'player1')
        
        # Game should be over after correct guess
        assert game.is_game_over() is True
    
    def test_get_winner(self):
        """Test that winner is returned correctly."""
        word_list = ['HELLO', 'WORLD', 'PYTHON']
        game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
        
        game.add_player('player1', 'Alice')
        game.add_player('player2', 'Bob')
        game.start_game()
        
        # No winner initially
        assert game.get_winner() is None
        
        # Make a correct guess
        game.answer = 'HELLO'
        game.make_guess('HELLO', 'player1')
        
        # Player1 should be the winner
        assert game.get_winner() == 'player1'


if __name__ == '__main__':
    pytest.main([__file__]) 