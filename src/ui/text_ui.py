"""
Text-based UI for the Wordle game.

This module provides a simple command-line interface for playing Wordle.
"""

from typing import Dict, Any
from ..core.game_engine import LetterResult


class TextUI:
    """
    Text-based user interface for the Wordle game.
    
    This class provides a simple command-line interface for playing
    different game modes of Wordle.
    """
    
    def __init__(self):
        """Initialize the text UI."""
        self.letter_colors = {
            LetterResult.HIT: '🟩',      # Green square
            LetterResult.PRESENT: '🟨',  # Yellow square
            LetterResult.MISS: '⬜'       # White square
        }
    
    def run_game(self, game):
        """
        Run the game with the text UI.
        
        Args:
            game: The game instance to run
        """
        print("\n" + "="*50)
        print("🎯 WELCOME TO WORDLE!")
        print("="*50)
        print("\nHow to play:")
        print("🟩 Green = Letter is correct and in right position")
        print("🟨 Yellow = Letter is in the word but wrong position")
        print("⬜ White = Letter is not in the word")
        print("\n" + "="*50)
        
        while not game.is_game_over():
            self._display_game_state(game)
            self._get_and_process_guess(game)
        
        self._display_final_result(game)
    
    def _display_game_state(self, game):
        """Display the current game state."""
        state = game.get_game_state()
        
        print(f"\nRound {state['current_round'] + 1}/{state['max_rounds']}")
        print(f"Remaining guesses: {state['remaining_rounds']}")
        
        # Display previous guesses
        if state['guesses']:
            print("\nPrevious guesses:")
            for i, (guess, result) in enumerate(zip(state['guesses'], state['results'])):
                self._display_guess_result(guess, result, i + 1)
        
        # Display empty grid for remaining rounds
        remaining = state['max_rounds'] - len(state['guesses'])
        for i in range(remaining):
            print(f"{len(state['guesses']) + i + 1}. {'_' * 5}")
    
    def _display_guess_result(self, guess, result, round_num):
        """Display a guess and its result."""
        result_str = ''.join([self.letter_colors[r] for r in result])
        print(f"{round_num}. {guess} {result_str}")
    
    def _get_and_process_guess(self, game):
        """Get a guess from the user and process it."""
        while True:
            try:
                guess = input("\nEnter your guess (5 letters): ").strip().upper()
                
                if len(guess) != 5:
                    print("❌ Guess must be exactly 5 letters!")
                    continue
                
                if not guess.isalpha():
                    print("❌ Guess must contain only letters!")
                    continue
                
                # Make the guess
                result = game.make_guess(guess)
                
                if result['success']:
                    # Display the result
                    print(f"\n{guess} {''.join([self.letter_colors[r] for r in result['result']])}")
                    
                    if result['is_correct']:
                        print("\n🎉 CONGRATULATIONS! You got it!")
                    elif result['game_state'] == 'lost':
                        print(f"\n😔 Game Over! The word was {game.get_answer()}")
                    
                    break
                else:
                    print(f"❌ {result['error']}")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for playing!")
                exit(0)
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _display_final_result(self, game):
        """Display the final game result."""
        state = game.get_game_state()
        
        print("\n" + "="*50)
        print("GAME OVER!")
        print("="*50)
        
        if state['game_state'] == 'won':
            print(f"🎉 You won in {state['current_round']} rounds!")
        else:
            print(f"😔 You lost! The word was {state['answer']}")
        
        print(f"\nFinal score: {state['current_round']}/{state['max_rounds']}")
        
        # Display all guesses
        print("\nYour guesses:")
        for i, (guess, result) in enumerate(zip(state['guesses'], state['results'])):
            self._display_guess_result(guess, result, i + 1)
        
        print("\n" + "="*50)
        print("Thanks for playing! 👋")
        print("="*50) 