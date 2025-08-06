#!/usr/bin/env python3
"""
Simple test script for multiplayer functionality.
"""

import sys
import os

# Change to src directory
os.chdir(os.path.join(os.path.dirname(__file__), 'src'))

from game_modes.multiplayer import MultiplayerGame

def test_multiplayer():
    """Test basic multiplayer functionality."""
    print("🧪 Testing Multiplayer Game...")
    
    # Create game
    word_list = ['HELLO', 'WORLD', 'SPACE', 'BEACH', 'DREAM']
    game = MultiplayerGame(word_list, max_rounds=6, max_players=4)
    
    print("✅ Game created successfully")
    
    # Add players
    result1 = game.add_player('player1', 'Alice')
    print(f"✅ {result1['message']}")
    
    result2 = game.add_player('player2', 'Bob')
    print(f"✅ {result2['message']}")
    
    # Start game
    game.start_game()
    print("✅ Game started successfully")
    
    # Make a guess
    guess_result = game.make_guess('WORLD', 'player1')
    print(f"✅ Player 1 guessed: {guess_result['success']}")
    
    # Get game state
    state = game.get_game_state()
    print(f"✅ Game state: {state['game_state']}")
    
    print("🎉 All tests passed!")

if __name__ == '__main__':
    test_multiplayer() 