"""
Single player Wordle game mode.

This module implements the basic single player Wordle game as described in Task 1.
"""

from typing import List, Dict, Any, Optional
from .base_game_mode import BaseGameMode
from ..core.game_engine import LetterResult, GameState


class SinglePlayerGame(BaseGameMode):
    """
    Single player Wordle game implementation.
    
    This implements the basic Wordle game as described in Task 1:
    - Player guesses a 5-letter word
    - Game provides feedback (Hit/Present/Miss)
    - Player wins if they guess correctly within max rounds
    - Player loses if they run out of rounds
    """
    
    def __init__(self, word_list: List[str], max_rounds: int = 6):
        """
        Initialize the single player game.
        
        Args:
            word_list: List of valid 5-letter words
            max_rounds: Maximum number of guessing rounds
        """
        super().__init__(word_list, max_rounds)
        self.player_name = "Player"
    
    def start_game(self, answer: Optional[str] = None, player_name: str = "Player") -> None:
        """
        Start a new single player game.
        
        Args:
            answer: The word to guess (if None, randomly selected)
            player_name: Name of the player
        """
        self.player_name = player_name
        self.game.start_new_game(answer)
    
    def make_guess(self, guess: str) -> Dict[str, Any]:
        """
        Make a guess in the single player game.
        
        Args:
            guess: The word to guess
            
        Returns:
            Dictionary containing the result of the guess
        """
        try:
            result, is_correct = self.game.make_guess(guess)
            
            return {
                'success': True,
                'result': result,
                'is_correct': is_correct,
                'round': self.game.get_current_round(),
                'remaining_rounds': self.game.get_remaining_rounds(),
                'game_state': self.game.get_game_state().value
            }
        except ValueError as e:
            return {
                'success': False,
                'error': str(e),
                'round': self.game.get_current_round(),
                'remaining_rounds': self.game.get_remaining_rounds()
            }
        except RuntimeError as e:
            return {
                'success': False,
                'error': str(e),
                'round': self.game.get_current_round(),
                'remaining_rounds': self.game.get_remaining_rounds()
            }
    
    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current state of the single player game.
        
        Returns:
            Dictionary containing the current game state
        """
        return {
            'game_state': self.game.get_game_state().value,
            'current_round': self.game.get_current_round(),
            'max_rounds': self.max_rounds,
            'remaining_rounds': self.game.get_remaining_rounds(),
            'guesses': self.game.get_guesses(),
            'results': self.game.get_results(),
            'answer': self.game.get_answer(),
            'player_name': self.player_name,
            'is_game_over': self.game.is_game_over()
        }
    
    def is_game_over(self) -> bool:
        """
        Check if the single player game is over.
        
        Returns:
            True if the game is over, False otherwise
        """
        return self.game.is_game_over()
    
    def get_winner(self) -> Optional[str]:
        """
        Get the winner of the single player game.
        
        Returns:
            Player name if they won, None otherwise
        """
        if self.game.get_game_state() == GameState.WON:
            return self.player_name
        return None
    
    def get_game_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the game results.
        
        Returns:
            Dictionary containing game summary
        """
        game_state = self.game.get_game_state()
        
        summary = {
            'player_name': self.player_name,
            'game_state': game_state.value,
            'total_rounds': self.game.get_current_round(),
            'max_rounds': self.max_rounds,
            'guesses': self.game.get_guesses(),
            'results': self.game.get_results(),
            'answer': self.game.get_answer()
        }
        
        if game_state == GameState.WON:
            summary['result'] = 'WON'
            summary['rounds_to_win'] = self.game.get_current_round()
        elif game_state == GameState.LOST:
            summary['result'] = 'LOST'
            summary['rounds_played'] = self.game.get_current_round()
        else:
            summary['result'] = 'IN_PROGRESS'
        
        return summary 