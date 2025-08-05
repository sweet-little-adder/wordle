#!/usr/bin/env python3
"""
Main entry point for the Wordle game.

This module provides the command line interface for running different
game modes and serves as the main entry point for the application.
"""

import argparse
import sys
import os
from typing import List

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.game_engine import LetterResult
from game_modes.single_player import SinglePlayerGame
from game_modes.cheating_host import CheatingHostGame
from utils.word_loader import get_default_word_list
from ui.text_ui import TextUI


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Wordle Game')
    
    parser.add_argument(
        '--mode',
        choices=['single', 'cheating', 'server', 'client', 'multiplayer'],
        default='single',
        help='Game mode to play (default: single)'
    )
    
    parser.add_argument(
        '--max-rounds',
        type=int,
        default=6,
        help='Maximum number of rounds (default: 6)'
    )
    
    parser.add_argument(
        '--word-list',
        type=str,
        help='Path to custom word list file'
    )
    
    parser.add_argument(
        '--answer',
        type=str,
        help='Specific answer word (for testing)'
    )
    
    # Server/Client specific arguments
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Server host (for client mode)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Server port (for server/client mode)'
    )
    
    # Multiplayer specific arguments
    parser.add_argument(
        '--players',
        type=int,
        default=2,
        help='Number of players (for multiplayer mode)'
    )
    
    return parser.parse_args()


def load_word_list(args) -> List[str]:
    """Load the word list based on command line arguments."""
    if args.word_list:
        try:
            from utils.word_loader import load_word_list
            return load_word_list(args.word_list)
        except Exception as e:
            print(f"Error loading word list: {e}")
            print("Falling back to default word list.")
            return get_default_word_list()
    else:
        return get_default_word_list()


def create_game_mode(args, word_list: List[str]):
    """Create the appropriate game mode based on arguments."""
    if args.mode == 'single':
        return SinglePlayerGame(word_list, args.max_rounds)
    elif args.mode == 'cheating':
        return CheatingHostGame(word_list, args.max_rounds)
    elif args.mode == 'server':
        # TODO: Implement server mode
        print("Server mode not yet implemented")
        sys.exit(1)
    elif args.mode == 'client':
        # TODO: Implement client mode
        print("Client mode not yet implemented")
        sys.exit(1)
    elif args.mode == 'multiplayer':
        # TODO: Implement multiplayer mode
        print("Multiplayer mode not yet implemented")
        sys.exit(1)
    else:
        raise ValueError(f"Unknown game mode: {args.mode}")


def main():
    """Main entry point for the Wordle game."""
    args = parse_arguments()
    
    try:
        # Load word list
        word_list = load_word_list(args)
        print(f"Loaded {len(word_list)} words")
        
        # Create game mode
        game = create_game_mode(args, word_list)
        
        # Create UI
        ui = TextUI()
        
        # Start game
        if args.mode == 'single':
            game.start_game(answer=args.answer)
        elif args.mode == 'cheating':
            game.start_game()
        
        # Run the game
        ui.run_game(game)
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 