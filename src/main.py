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
from game_modes.server_client import ServerGame, ClientGame
from game_modes.multiplayer import MultiplayerGame
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
        return ServerGame(word_list, args.max_rounds, args.port)
    elif args.mode == 'client':
        server_url = f"http://{args.host}:{args.port}"
        return ClientGame(word_list, args.max_rounds, server_url)
    elif args.mode == 'multiplayer':
        return MultiplayerGame(word_list, args.max_rounds, args.players)
    else:
        raise ValueError(f"Unknown game mode: {args.mode}")


def run_server_mode(game: ServerGame, args):
    """Run the server mode."""
    print(f"🚀 Starting Wordle server on port {args.port}")
    print(f"📊 Server will be available at http://localhost:{args.port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        game.start_server(host='0.0.0.0', debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")


def run_client_mode(game: ClientGame, args):
    """Run the client mode."""
    print(f"🔗 Connecting to server at http://{args.host}:{args.port}")
    
    try:
        # Start a game
        game.start_game(mode='single')
        print("✅ Connected to server successfully")
        
        # Create UI and run game
        ui = TextUI()
        ui.run_game(game)
        
    except Exception as e:
        print(f"❌ Failed to connect to server: {e}")
        print("Make sure the server is running first with: python src/main.py --mode server")


def run_multiplayer_mode(game: MultiplayerGame, args):
    """Run the multiplayer mode."""
    print(f"🎮 Starting multiplayer game with {args.players} players")
    print("This is a text-based multiplayer mode.")
    print("Players will take turns making guesses.")
    
    # Add players
    for i in range(args.players):
        player_id = f"player_{i+1}"
        player_name = f"Player {i+1}"
        result = game.add_player(player_id, player_name)
        print(f"✅ {result['message']}")
    
    # Start the game
    game.start_game()
    
    # Create UI and run game
    ui = TextUI()
    ui.run_multiplayer_game(game)


def main():
    """Main entry point for the Wordle game."""
    args = parse_arguments()
    
    try:
        # Load word list
        word_list = load_word_list(args)
        print(f"📚 Loaded {len(word_list)} words")
        
        # Create game mode
        game = create_game_mode(args, word_list)
        
        # Run appropriate mode
        if args.mode == 'server':
            run_server_mode(game, args)
        elif args.mode == 'client':
            run_client_mode(game, args)
        elif args.mode == 'multiplayer':
            run_multiplayer_mode(game, args)
        else:
            # Single player or cheating mode
            ui = TextUI()
            
            # Start game
            if args.mode == 'single':
                game.start_game(answer=args.answer)
            elif args.mode == 'cheating':
                game.start_game()
            
            # Run the game
            ui.run_game(game)
        
    except KeyboardInterrupt:
        print("\n🛑 Game interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 