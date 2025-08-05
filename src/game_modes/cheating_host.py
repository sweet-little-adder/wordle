"""
Cheating host Wordle game mode.

This module implements the cheating host Wordle game as described in Task 3.
The host adapts the answer based on player guesses to make the game more challenging.
"""

from typing import List, Dict, Any, Optional, Tuple
from .base_game_mode import BaseGameMode
from ..core.game_engine import LetterResult, GameState
from ..utils.word_loader import filter_words_by_pattern


class CheatingHostGame(BaseGameMode):
    """
    Cheating host Wordle game implementation.
    
    This implements the Absurdle-style cheating host as described in Task 3:
    - Host doesn't select an answer at the beginning
    - Host maintains a list of candidate words
    - After each guess, host filters candidates and selects the worst possible answer
    - Scoring prioritizes hits over presents
    """
    
    def __init__(self, word_list: List[str], max_rounds: int = 6):
        """
        Initialize the cheating host game.
        
        Args:
            word_list: List of valid 5-letter words
            max_rounds: Maximum number of guessing rounds
        """
        super().__init__(word_list, max_rounds)
        self.candidate_words = word_list.copy()
        self.answer = None
        self.player_name = "Player"
    
    def start_game(self, player_name: str = "Player") -> None:
        """
        Start a new cheating host game.
        
        Args:
            player_name: Name of the player
        """
        self.player_name = player_name
        self.candidate_words = self.word_list.copy()
        self.answer = None
        self.game = WordleGame(self.word_list, self.max_rounds)
        # Don't set an answer yet - it will be determined after the first guess
    
    def make_guess(self, guess: str) -> Dict[str, Any]:
        """
        Make a guess in the cheating host game.
        
        Args:
            guess: The word to guess
            
        Returns:
            Dictionary containing the result of the guess
        """
        try:
            if not self.validate_guess(guess):
                return {
                    'success': False,
                    'error': f"Invalid guess: {guess}",
                    'round': self.game.get_current_round(),
                    'remaining_rounds': self.game.get_remaining_rounds()
                }
            
            guess = guess.upper()
            
            # If this is the first guess, we need to determine the answer
            if self.answer is None:
                self._determine_answer(guess)
            
            # Now make the guess with the determined answer
            result, is_correct = self.game.make_guess(guess)
            
            return {
                'success': True,
                'result': result,
                'is_correct': is_correct,
                'round': self.game.get_current_round(),
                'remaining_rounds': self.game.get_remaining_rounds(),
                'game_state': self.game.get_game_state().value,
                'candidates_remaining': len(self.candidate_words)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'round': self.game.get_current_round(),
                'remaining_rounds': self.game.get_remaining_rounds()
            }
    
    def _determine_answer(self, guess: str) -> None:
        """
        Determine the answer based on the first guess.
        
        This is the core of the cheating host logic. We find the word
        that gives the worst possible result for the player's guess.
        
        Args:
            guess: The player's first guess
        """
        # Calculate the worst possible result for this guess
        worst_result = self._find_worst_result(guess)
        
        # Filter candidates to only include words that could produce this result
        self.candidate_words = filter_words_by_pattern(
            self.candidate_words, guess, worst_result
        )
        
        # Select the answer from remaining candidates
        self.answer = self.candidate_words[0] if self.candidate_words else None
        
        if self.answer:
            # Start the game with this answer
            self.game.start_new_game(self.answer)
    
    def _find_worst_result(self, guess: str) -> List[LetterResult]:
        """
        Find the worst possible result for a given guess.
        
        The worst result is the one that gives the player the least information,
        prioritizing hits over presents (as per the assignment requirements).
        
        Args:
            guess: The word to find the worst result for
            
        Returns:
            List of LetterResult representing the worst possible result
        """
        worst_score = -1
        worst_result = None
        
        for candidate in self.candidate_words:
            # Calculate what result this candidate would give for the guess
            result = self._calculate_result_for_candidate(guess, candidate)
            score = self._score_result(result)
            
            # Update worst result if this score is worse (lower)
            if score < worst_score or worst_result is None:
                worst_score = score
                worst_result = result
        
        return worst_result
    
    def _calculate_result_for_candidate(self, guess: str, candidate: str) -> List[LetterResult]:
        """
        Calculate the result that a candidate word would give for a guess.
        
        Args:
            guess: The guessed word
            candidate: The candidate word to test against
            
        Returns:
            List of LetterResult for the guess against this candidate
        """
        result = [LetterResult.MISS] * 5
        answer_letters = list(candidate)
        guess_letters = list(guess)
        
        # First pass: Mark hits
        for i in range(5):
            if guess_letters[i] == answer_letters[i]:
                result[i] = LetterResult.HIT
                answer_letters[i] = None
                guess_letters[i] = None
        
        # Second pass: Mark presents
        for i in range(5):
            if guess_letters[i] is not None:
                if guess_letters[i] in answer_letters:
                    result[i] = LetterResult.PRESENT
                    answer_letters[answer_letters.index(guess_letters[i])] = None
        
        return result
    
    def _score_result(self, result: List[LetterResult]) -> int:
        """
        Score a result based on the assignment requirements.
        
        The scoring prioritizes hits over presents:
        - More hits = higher score
        - If same number of hits, more presents = higher score
        
        Args:
            result: List of LetterResult to score
            
        Returns:
            Integer score (higher is better for the player)
        """
        hits = sum(1 for r in result if r == LetterResult.HIT)
        presents = sum(1 for r in result if r == LetterResult.PRESENT)
        
        # Prioritize hits over presents (hits are worth more)
        return hits * 10 + presents
    
    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current state of the cheating host game.
        
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
            'is_game_over': self.game.is_game_over(),
            'candidates_remaining': len(self.candidate_words)
        }
    
    def is_game_over(self) -> bool:
        """
        Check if the cheating host game is over.
        
        Returns:
            True if the game is over, False otherwise
        """
        return self.game.is_game_over()
    
    def get_winner(self) -> Optional[str]:
        """
        Get the winner of the cheating host game.
        
        Returns:
            Player name if they won, None otherwise
        """
        if self.game.get_game_state() == GameState.WON:
            return self.player_name
        return None
    
    def get_game_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the cheating host game results.
        
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
            'answer': self.game.get_answer(),
            'candidates_remaining': len(self.candidate_words)
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