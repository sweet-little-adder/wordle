"""
Core Wordle game engine.

This module contains the fundamental game logic for Wordle, including:
- Word validation and scoring
- Game state management
- Win/lose condition checking
"""

from typing import List, Tuple, Optional, Dict
from enum import Enum
import random


class LetterResult(Enum):
    """Enumeration for letter scoring results."""
    HIT = "hit"      # Letter is in correct position (green)
    PRESENT = "present"  # Letter is in word but wrong position (yellow)
    MISS = "miss"    # Letter is not in word (gray)


class GameState(Enum):
    """Enumeration for game states."""
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class WordleGame:
    """
    Core Wordle game engine.
    
    This class implements the fundamental game logic for Wordle, including
    word validation, scoring, and game state management.
    """
    
    def __init__(self, word_list: List[str], max_rounds: int = 6):
        """
        Initialize a new Wordle game.
        
        Args:
            word_list: List of valid 5-letter words
            max_rounds: Maximum number of guessing rounds (default: 6)
        """
        self.word_list = [word.upper() for word in word_list]
        self.max_rounds = max_rounds
        self.answer = None
        self.current_round = 0
        self.guesses = []
        self.results = []
        self.game_state = GameState.PLAYING
        
        # Validate word list
        self._validate_word_list()
    
    def _validate_word_list(self) -> None:
        """Validate that all words in the word list are 5 letters and alphabetic."""
        if not self.word_list:
            raise ValueError("Word list cannot be empty")
        
        for word in self.word_list:
            if not word.isalpha() or len(word) != 5:
                raise ValueError(f"Invalid word in word list: {word}")
    
    def start_new_game(self, answer: Optional[str] = None) -> None:
        """
        Start a new game with the given answer or a random word.
        
        Args:
            answer: The word to guess (if None, randomly selected from word list)
        """
        if answer is not None:
            answer = answer.upper()
            if answer not in self.word_list:
                raise ValueError(f"Answer '{answer}' is not in the word list")
            self.answer = answer
        else:
            self.answer = random.choice(self.word_list)
        
        self.current_round = 0
        self.guesses = []
        self.results = []
        self.game_state = GameState.PLAYING
    
    def is_valid_guess(self, guess: str) -> bool:
        """
        Check if a guess is valid.
        
        Args:
            guess: The word to validate
            
        Returns:
            True if the guess is valid, False otherwise
        """
        guess = guess.upper()
        return (len(guess) == 5 and 
                guess.isalpha() and 
                guess in self.word_list)
    
    def make_guess(self, guess: str) -> Tuple[List[LetterResult], bool]:
        """
        Make a guess and return the result.
        
        Args:
            guess: The word to guess
            
        Returns:
            Tuple of (letter results, is_correct)
            
        Raises:
            ValueError: If the guess is invalid
            RuntimeError: If the game is already over
        """
        if self.game_state != GameState.PLAYING:
            raise RuntimeError("Game is already over")
        
        if not self.is_valid_guess(guess):
            raise ValueError(f"Invalid guess: {guess}")
        
        guess = guess.upper()
        self.guesses.append(guess)
        self.current_round += 1
        
        # Calculate result
        result = self._calculate_result(guess)
        self.results.append(result)
        
        # Check if guess is correct
        is_correct = guess == self.answer
        
        # Update game state
        if is_correct:
            self.game_state = GameState.WON
        elif self.current_round >= self.max_rounds:
            self.game_state = GameState.LOST
        
        return result, is_correct
    
    def _calculate_result(self, guess: str) -> List[LetterResult]:
        """
        Calculate the result for a guess.
        
        This implements the exact Wordle scoring logic:
        1. First pass: Mark all hits (correct letter, correct position)
        2. Second pass: Mark presents (correct letter, wrong position)
        3. Remaining letters are misses
        
        Args:
            guess: The guessed word
            
        Returns:
            List of LetterResult for each position
        """
        result = [LetterResult.MISS] * 5
        answer_letters = list(self.answer)
        guess_letters = list(guess)
        
        # First pass: Mark hits
        for i in range(5):
            if guess_letters[i] == answer_letters[i]:
                result[i] = LetterResult.HIT
                answer_letters[i] = None  # Mark as used
                guess_letters[i] = None   # Mark as used
        
        # Second pass: Mark presents
        for i in range(5):
            if guess_letters[i] is not None:
                if guess_letters[i] in answer_letters:
                    result[i] = LetterResult.PRESENT
                    # Remove the first occurrence from answer
                    answer_letters[answer_letters.index(guess_letters[i])] = None
        
        return result
    
    def get_game_state(self) -> GameState:
        """Get the current game state."""
        return self.game_state
    
    def get_current_round(self) -> int:
        """Get the current round number."""
        return self.current_round
    
    def get_remaining_rounds(self) -> int:
        """Get the number of remaining rounds."""
        return max(0, self.max_rounds - self.current_round)
    
    def get_guesses(self) -> List[str]:
        """Get all previous guesses."""
        return self.guesses.copy()
    
    def get_results(self) -> List[List[LetterResult]]:
        """Get all previous results."""
        return [result.copy() for result in self.results]
    
    def get_answer(self) -> Optional[str]:
        """Get the answer (only if game is over)."""
        if self.game_state != GameState.PLAYING:
            return self.answer
        return None
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_state != GameState.PLAYING
    
    def get_game_summary(self) -> Dict:
        """
        Get a summary of the current game state.
        
        Returns:
            Dictionary containing game state information
        """
        return {
            'game_state': self.game_state.value,
            'current_round': self.current_round,
            'max_rounds': self.max_rounds,
            'remaining_rounds': self.get_remaining_rounds(),
            'guesses': self.guesses.copy(),
            'results': [result.copy() for result in self.results],
            'answer': self.get_answer(),
            'is_game_over': self.is_game_over()
        } 