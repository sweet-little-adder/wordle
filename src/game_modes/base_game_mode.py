"""
Base game mode interface.

This module defines the abstract base class for all game modes,
ensuring a consistent interface across different implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..core.game_engine import WordleGame, LetterResult, GameState


class BaseGameMode(ABC):
    """
    Abstract base class for all game modes.
    
    This class defines the interface that all game modes must implement,
    ensuring consistency across different game implementations.
    """
    
    def __init__(self, word_list: List[str], max_rounds: int = 6):
        """
        Initialize the game mode.
        
        Args:
            word_list: List of valid 5-letter words
            max_rounds: Maximum number of guessing rounds
        """
        self.word_list = word_list
        self.max_rounds = max_rounds
        self.game = WordleGame(word_list, max_rounds)
    
    @abstractmethod
    def start_game(self, **kwargs) -> None:
        """
        Start a new game.
        
        Args:
            **kwargs: Additional arguments specific to the game mode
        """
        pass
    
    @abstractmethod
    def make_guess(self, guess: str, **kwargs) -> Dict[str, Any]:
        """
        Make a guess in the game.
        
        Args:
            guess: The word to guess
            **kwargs: Additional arguments specific to the game mode
            
        Returns:
            Dictionary containing the result of the guess
        """
        pass
    
    @abstractmethod
    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current state of the game.
        
        Returns:
            Dictionary containing the current game state
        """
        pass
    
    @abstractmethod
    def is_game_over(self) -> bool:
        """
        Check if the game is over.
        
        Returns:
            True if the game is over, False otherwise
        """
        pass
    
    @abstractmethod
    def get_winner(self) -> Optional[str]:
        """
        Get the winner of the game (if applicable).
        
        Returns:
            Winner identifier or None if no winner
        """
        pass
    
    def validate_guess(self, guess: str) -> bool:
        """
        Validate a guess.
        
        Args:
            guess: The word to validate
            
        Returns:
            True if the guess is valid, False otherwise
        """
        return self.game.is_valid_guess(guess)
    
    def get_remaining_rounds(self) -> int:
        """
        Get the number of remaining rounds.
        
        Returns:
            Number of remaining rounds
        """
        return self.game.get_remaining_rounds()
    
    def get_current_round(self) -> int:
        """
        Get the current round number.
        
        Returns:
            Current round number
        """
        return self.game.get_current_round()
    
    def get_guesses(self) -> List[str]:
        """
        Get all previous guesses.
        
        Returns:
            List of all previous guesses
        """
        return self.game.get_guesses()
    
    def get_results(self) -> List[List[LetterResult]]:
        """
        Get all previous results.
        
        Returns:
            List of all previous results
        """
        return self.game.get_results()
    
    def get_answer(self) -> Optional[str]:
        """
        Get the answer (only if game is over).
        
        Returns:
            The answer word or None if game is still in progress
        """
        return self.game.get_answer() 