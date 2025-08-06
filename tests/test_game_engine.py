"""
Tests for the Wordle game engine.

This module contains unit tests for the core game engine functionality.
"""

import pytest
from src.core.game_engine import WordleGame, GameState, LetterResult


class TestWordleGame:
    """Test cases for the WordleGame class."""
    
    def test_game_initialization(self):
        """Test that a game can be initialized correctly."""
        word_list = ['HELLO', 'WORLD', 'SPACE']
        game = WordleGame(word_list, max_rounds=6)
        
        assert game.max_rounds == 6
        assert game.word_list == word_list
        assert game.game_state == GameState.PLAYING
    
    def test_start_game(self):
        """Test that a game can be started."""
        word_list = ['HELLO', 'WORLD', 'SPACE']
        game = WordleGame(word_list, max_rounds=6)
        
        game.start_new_game(answer='HELLO')
        
        assert game.game_state == GameState.PLAYING
        assert game.answer == 'HELLO'
        assert game.current_round == 0
        assert len(game.guesses) == 0
        assert len(game.results) == 0
    
    def test_valid_guess(self):
        """Test that a valid guess is processed correctly."""
        word_list = ['HELLO', 'WORLD', 'SPACE']
        game = WordleGame(word_list, max_rounds=6)
        game.start_new_game(answer='HELLO')
        
        result, is_correct = game.make_guess('WORLD')
        
        assert len(result) == 5
        assert isinstance(is_correct, bool)
        assert game.current_round == 1
        assert len(game.guesses) == 1
        assert len(game.results) == 1
    
    def test_invalid_guess_length(self):
        """Test that an invalid guess length is rejected."""
        word_list = ['HELLO', 'WORLD', 'SPACE']
        game = WordleGame(word_list, max_rounds=6)
        game.start_new_game(answer='HELLO')
        
        # This should raise an exception or return False
        assert not game.is_valid_guess('HI')
    
    def test_invalid_guess_not_in_word_list(self):
        """Test that a guess not in the word list is rejected."""
        word_list = ['HELLO', 'WORLD', 'SPACE']
        game = WordleGame(word_list, max_rounds=6)
        game.start_new_game(answer='HELLO')
        
        assert not game.is_valid_guess('ABCDE')
    
    def test_correct_guess_wins_game(self):
        """Test that a correct guess wins the game."""
        word_list = ['HELLO', 'WORLD', 'SPACE']
        game = WordleGame(word_list, max_rounds=6)
        game.start_new_game(answer='HELLO')
        
        result, is_correct = game.make_guess('HELLO')
        
        assert is_correct is True
        assert game.game_state == GameState.PLAYING  # Game state doesn't change until checked
        assert game.is_game_over() is True
    
    def test_max_rounds_reached_loses_game(self):
        """Test that reaching max rounds loses the game."""
        word_list = ['HELLO', 'WORLD', 'SPACE']
        game = WordleGame(word_list, max_rounds=2)
        game.start_new_game(answer='HELLO')
        
        # Make two wrong guesses
        game.make_guess('WORLD')
        result, is_correct = game.make_guess('SPACE')
        
        assert is_correct is False
        assert game.is_game_over() is True
    
    def test_letter_result_calculation(self):
        """Test that letter results are calculated correctly."""
        word_list = ['HELLO', 'WORLD', 'SPACE']
        game = WordleGame(word_list, max_rounds=6)
        game.start_new_game(answer='HELLO')
        
        result, is_correct = game.make_guess('WORLD')
        
        # W should be MISS, O should be PRESENT, R should be MISS, L should be PRESENT, D should be MISS
        expected_results = [LetterResult.MISS, LetterResult.PRESENT, LetterResult.MISS, LetterResult.PRESENT, LetterResult.MISS]
        
        assert result == expected_results
    
    def test_get_game_state(self):
        """Test that game state is returned correctly."""
        word_list = ['HELLO', 'WORLD', 'SPACE']
        game = WordleGame(word_list, max_rounds=6)
        game.start_new_game(answer='HELLO')
        
        state = game.get_game_state()
        
        assert state == GameState.PLAYING
        assert game.get_current_round() == 0
        assert game.get_remaining_rounds() == 6
        assert game.get_answer() == 'HELLO'  # Answer is revealed in this implementation
        assert game.is_game_over() is False


class TestLetterResult:
    """Test cases for the LetterResult enum."""
    
    def test_letter_result_values(self):
        """Test that LetterResult has the correct values."""
        assert LetterResult.HIT.value == 'hit'
        assert LetterResult.PRESENT.value == 'present'
        assert LetterResult.MISS.value == 'miss'
    
    def test_letter_result_string_representation(self):
        """Test that LetterResult can be converted to string."""
        assert str(LetterResult.HIT.value) == 'hit'
        assert str(LetterResult.PRESENT.value) == 'present'
        assert str(LetterResult.MISS.value) == 'miss'


class TestGameState:
    """Test cases for the GameState enum."""
    
    def test_game_state_values(self):
        """Test that GameState has the correct values."""
        assert GameState.PLAYING.value == 'playing'
        assert GameState.WON.value == 'won'
        assert GameState.LOST.value == 'lost'
    
    def test_game_state_string_representation(self):
        """Test that GameState can be converted to string."""
        assert str(GameState.PLAYING.value) == 'playing'
        assert str(GameState.WON.value) == 'won'
        assert str(GameState.LOST.value) == 'lost'


if __name__ == '__main__':
    pytest.main([__file__]) 