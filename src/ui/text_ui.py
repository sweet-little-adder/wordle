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
    
    def run_multiplayer_game(self, game):
        """
        Run the multiplayer game with the text UI.
        
        Args:
            game: The multiplayer game instance to run
        """
        print("\n" + "="*50)
        print("🎮 WELCOME TO MULTIPLAYER WORDLE!")
        print("="*50)
        print("\nHow to play:")
        print("🟩 Green = Letter is correct and in right position")
        print("🟨 Yellow = Letter is in the word but wrong position")
        print("⬜ White = Letter is not in the word")
        print("\nPlayers take turns making guesses.")
        print("First player to guess correctly wins!")
        print("\n" + "="*50)
        
        while not game.is_game_over():
            self._display_multiplayer_state(game)
            self._get_and_process_multiplayer_guess(game)
        
        self._display_multiplayer_final_result(game)
    
    def _display_multiplayer_state(self, game):
        """Display the current multiplayer game state."""
        state = game.get_game_state()
        
        print(f"\n🎮 Round {state['current_round'] + 1}/{state['max_rounds']}")
        print(f"⏰ Time remaining: {state['remaining_time']:.1f}s")
        print(f"👥 Players: {state['player_count']}/{state['max_players']}")
        
        # Display leaderboard
        leaderboard = game.get_leaderboard()
        print("\n📊 Leaderboard:")
        for entry in leaderboard:
            status = "🏆" if entry['has_won'] else "🎯"
            print(f"  {entry['rank']}. {entry['player_name']} - {entry['score']} pts {status}")
        
        # Display each player's guesses
        print("\n📝 Player Progress:")
        for player_data in state['players']:
            player_id = player_data['id']
            player_state = game.get_player_state(player_id)
            
            print(f"\n  {player_data['name']}:")
            if player_state['guesses']:
                for i, (guess, result) in enumerate(zip(player_state['guesses'], player_state['results'])):
                    result_str = ''.join([self.letter_colors[r] for r in result])
                    print(f"    {i+1}. {guess} {result_str}")
            else:
                print(f"    No guesses yet")
    
    def _get_and_process_multiplayer_guess(self, game):
        """Get a guess from the current player and process it."""
        state = game.get_game_state()
        
        # Find current player (player with fewest guesses)
        current_player = None
        min_guesses = float('inf')
        
        for player_data in state['players']:
            player_id = player_data['id']
            player_state = game.get_player_state(player_id)
            if len(player_state['guesses']) < min_guesses:
                min_guesses = len(player_state['guesses'])
                current_player = player_id
        
        if not current_player:
            print("❌ No players available")
            return
        
        player_name = game.get_player_state(current_player)['player_name']
        print(f"\n🎯 {player_name}'s turn:")
        
        while True:
            try:
                guess = input(f"Enter {player_name}'s guess (5 letters): ").strip().upper()
                
                if len(guess) != 5:
                    print("❌ Guess must be exactly 5 letters!")
                    continue
                
                if not guess.isalpha():
                    print("❌ Guess must contain only letters!")
                    continue
                
                # Make the guess
                result = game.make_guess(guess, current_player)
                
                if result['success']:
                    # Display the result
                    print(f"\n{guess} {''.join([self.letter_colors[r] for r in result['result']])}")
                    
                    if result['is_correct']:
                        print(f"\n🎉 CONGRATULATIONS {player_name}! You won!")
                    elif result['game_state'] == 'lost':
                        print(f"\n😔 Game Over! The word was {state['answer']}")
                    
                    break
                else:
                    print(f"❌ {result['error']}")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for playing!")
                exit(0)
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _display_multiplayer_final_result(self, game):
        """Display the final multiplayer game result."""
        state = game.get_game_state()
        leaderboard = game.get_leaderboard()
        
        print("\n" + "="*50)
        print("🏁 GAME OVER!")
        print("="*50)
        
        if state['game_state'] == 'won':
            winner = game.get_winner()
            if winner:
                winner_name = game.get_player_state(winner)['player_name']
                winner_rounds = game.get_player_state(winner)['rounds_to_win']
                print(f"🎉 {winner_name} wins in {winner_rounds} rounds!")
        else:
            print(f"😔 No one guessed correctly! The word was {state['answer']}")
        
        print(f"\n📊 Final Leaderboard:")
        for entry in leaderboard:
            status = "🏆" if entry['has_won'] else "🎯"
            print(f"  {entry['rank']}. {entry['player_name']} - {entry['score']} pts {status}")
        
        print("\n" + "="*50)
        print("Thanks for playing! 👋")
        print("="*50)

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