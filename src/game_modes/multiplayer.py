"""
Multiplayer Wordle game mode.

This module implements the multiplayer Wordle game as described in Task 4.
Multiple players can compete against each other in real-time.
"""

import time
import random
from typing import List, Dict, Any, Optional, Set
from .base_game_mode import BaseGameMode
from ..core.game_engine import WordleGame, GameState, LetterResult


class MultiplayerGame(BaseGameMode):
    """
    Multiplayer Wordle game implementation.
    
    This implements a competitive multiplayer mode where:
    - Multiple players guess the same word
    - Players can see each other's progress
    - First player to guess correctly wins
    - If no one guesses correctly, player with best score wins
    """
    
    def __init__(self, word_list: List[str], max_rounds: int = 6, max_players: int = 4):
        """
        Initialize the multiplayer game.
        
        Args:
            word_list: List of valid 5-letter words
            max_rounds: Maximum number of guessing rounds
            max_players: Maximum number of players allowed
        """
        super().__init__(word_list, max_rounds)
        self.max_players = max_players
        self.players = {}  # player_id -> player_data
        self.answer = None
        self.game_state = GameState.PLAYING
        self.current_round = 0
        self.round_start_time = None
        self.round_duration = 30  # seconds per round
        
    def add_player(self, player_id: str, player_name: str) -> Dict[str, Any]:
        """
        Add a player to the game.
        
        Args:
            player_id: Unique player identifier
            player_name: Display name for the player
            
        Returns:
            Dictionary with player info and game state
        """
        if len(self.players) >= self.max_players:
            return {
                'success': False,
                'error': f"Game is full. Maximum {self.max_players} players allowed."
            }
        
        if player_id in self.players:
            return {
                'success': False,
                'error': f"Player {player_id} is already in the game."
            }
        
        player_data = {
            'id': player_id,
            'name': player_name,
            'guesses': [],
            'results': [],
            'score': 0,
            'is_connected': True,
            'last_activity': time.time(),
            'has_won': False,
            'rounds_to_win': None
        }
        
        self.players[player_id] = player_data
        
        return {
            'success': True,
            'player_id': player_id,
            'player_name': player_name,
            'game_state': self.get_game_state(),
            'message': f"Player {player_name} joined the game"
        }
    
    def remove_player(self, player_id: str) -> Dict[str, Any]:
        """
        Remove a player from the game.
        
        Args:
            player_id: Player identifier to remove
            
        Returns:
            Dictionary with result info
        """
        if player_id not in self.players:
            return {
                'success': False,
                'error': f"Player {player_id} not found in game."
            }
        
        player_name = self.players[player_id]['name']
        del self.players[player_id]
        
        # Check if game should end due to insufficient players
        if len(self.players) < 2 and self.game_state == GameState.PLAYING:
            self.game_state = GameState.LOST
            return {
                'success': True,
                'message': f"Game ended: {player_name} left. Need at least 2 players.",
                'game_state': self.get_game_state()
            }
        
        return {
            'success': True,
            'message': f"Player {player_name} left the game",
            'game_state': self.get_game_state()
        }
    
    def start_game(self, **kwargs) -> None:
        """
        Start the multiplayer game.
        
        Args:
            **kwargs: Additional arguments (ignored)
        """
        if len(self.players) < 2:
            raise ValueError("Need at least 2 players to start the game.")
        
        # Select a random answer
        self.answer = random.choice(self.word_list)
        
        # Reset all players
        for player_data in self.players.values():
            player_data['guesses'] = []
            player_data['results'] = []
            player_data['score'] = 0
            player_data['has_won'] = False
            player_data['rounds_to_win'] = None
        
        self.game_state = GameState.PLAYING
        self.current_round = 0
        self.round_start_time = time.time()
        
        print(f"🎮 Multiplayer game started! Answer: {self.answer}")
    
    def make_guess(self, guess: str, player_id: str) -> Dict[str, Any]:
        """
        Make a guess for a specific player.
        
        Args:
            guess: The word to guess
            player_id: Player making the guess
            
        Returns:
            Dictionary containing the result of the guess
        """
        if player_id not in self.players:
            return {
                'success': False,
                'error': 'Player not found in game'
            }
        
        if self.game_state != GameState.PLAYING:
            return {
                'success': False,
                'error': 'Game is not in progress'
            }
        
        player_data = self.players[player_id]
        
        # Check if player already made a guess this round
        if len(player_data['guesses']) > self.current_round:
            return {
                'success': False,
                'error': 'Already made a guess this round'
            }
        
        # Validate guess
        if not self.validate_guess(guess):
            return {
                'success': False,
                'error': f'Invalid guess: {guess}'
            }
        
        guess = guess.upper()
        
        # Calculate result
        result = self._calculate_result(guess)
        
        # Update player data
        player_data['guesses'].append(guess)
        player_data['results'].append(result)
        player_data['last_activity'] = time.time()
        
        # Calculate score for this round
        round_score = self._calculate_round_score(result)
        player_data['score'] += round_score
        
        # Check if player won
        if guess == self.answer:
            player_data['has_won'] = True
            player_data['rounds_to_win'] = len(player_data['guesses'])
            self.game_state = GameState.WON
            return {
                'success': True,
                'result': result,
                'is_correct': True,
                'round_score': round_score,
                'total_score': player_data['score'],
                'game_state': self.get_game_state(),
                'message': f"🎉 {player_data['name']} wins in {len(player_data['guesses'])} rounds!"
            }
        
        # Check if round should end
        self._check_round_end()
        
        return {
            'success': True,
            'result': result,
            'is_correct': False,
            'round_score': round_score,
            'total_score': player_data['score'],
            'game_state': self.get_game_state()
        }
    
    def _calculate_result(self, guess: str) -> List[LetterResult]:
        """
        Calculate the result for a guess.
        
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
                answer_letters[i] = None
                guess_letters[i] = None
        
        # Second pass: Mark presents
        for i in range(5):
            if guess_letters[i] is not None:
                if guess_letters[i] in answer_letters:
                    result[i] = LetterResult.PRESENT
                    answer_letters[answer_letters.index(guess_letters[i])] = None
        
        return result
    
    def _calculate_round_score(self, result: List[LetterResult]) -> int:
        """
        Calculate the score for a round based on the result.
        
        Args:
            result: List of LetterResult for the guess
            
        Returns:
            Integer score for the round
        """
        hits = sum(1 for r in result if r == LetterResult.HIT)
        presents = sum(1 for r in result if r == LetterResult.PRESENT)
        
        # Scoring: hits are worth more than presents
        return hits * 10 + presents
    
    def _check_round_end(self) -> None:
        """Check if the current round should end."""
        # Check if all players have made their guesses
        all_guessed = all(len(player['guesses']) > self.current_round 
                         for player in self.players.values())
        
        # Check if round time limit is reached
        time_elapsed = time.time() - self.round_start_time
        time_expired = time_elapsed >= self.round_duration
        
        if all_guessed or time_expired:
            self.current_round += 1
            
            # Check if game should end
            if self.current_round >= self.max_rounds:
                self._end_game()
            else:
                self.round_start_time = time.time()
    
    def _end_game(self) -> None:
        """End the game and determine the winner."""
        if self.game_state == GameState.WON:
            return  # Game already ended with a winner
        
        # Find the player with the best score
        best_score = -1
        winner = None
        
        for player_id, player_data in self.players.items():
            if player_data['score'] > best_score:
                best_score = player_data['score']
                winner = player_id
        
        if winner:
            self.players[winner]['has_won'] = True
            self.game_state = GameState.WON
        
        print(f"🏁 Game ended! Winner: {self.players[winner]['name'] if winner else 'None'}")
    
    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current state of the multiplayer game.
        
        Returns:
            Dictionary containing the current game state
        """
        # Calculate remaining time in current round
        remaining_time = 0
        if self.round_start_time and self.game_state == GameState.PLAYING:
            elapsed = time.time() - self.round_start_time
            remaining_time = max(0, self.round_duration - elapsed)
        
        # Get player summaries (without revealing answers)
        player_summaries = []
        for player_data in self.players.values():
            summary = {
                'id': player_data['id'],
                'name': player_data['name'],
                'score': player_data['score'],
                'guesses_made': len(player_data['guesses']),
                'has_won': player_data['has_won'],
                'rounds_to_win': player_data['rounds_to_win'],
                'is_connected': player_data['is_connected'],
                'last_activity': player_data['last_activity']
            }
            player_summaries.append(summary)
        
        return {
            'game_state': self.game_state.value,
            'current_round': self.current_round,
            'max_rounds': self.max_rounds,
            'remaining_rounds': max(0, self.max_rounds - self.current_round),
            'remaining_time': remaining_time,
            'round_duration': self.round_duration,
            'players': player_summaries,
            'player_count': len(self.players),
            'max_players': self.max_players,
            'answer': self.answer if self.game_state != GameState.PLAYING else None,
            'is_game_over': self.game_state != GameState.PLAYING
        }
    
    def get_player_state(self, player_id: str) -> Dict[str, Any]:
        """
        Get the state for a specific player.
        
        Args:
            player_id: Player identifier
            
        Returns:
            Dictionary containing the player's game state
        """
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} not found")
        
        player_data = self.players[player_id]
        
        return {
            'player_id': player_id,
            'player_name': player_data['name'],
            'guesses': player_data['guesses'],
            'results': player_data['results'],
            'score': player_data['score'],
            'has_won': player_data['has_won'],
            'rounds_to_win': player_data['rounds_to_win'],
            'game_state': self.get_game_state()
        }
    
    def is_game_over(self) -> bool:
        """
        Check if the multiplayer game is over.
        
        Returns:
            True if the game is over, False otherwise
        """
        return self.game_state != GameState.PLAYING
    
    def get_winner(self) -> Optional[str]:
        """
        Get the winner of the multiplayer game.
        
        Returns:
            Winner player ID or None if no winner
        """
        for player_id, player_data in self.players.items():
            if player_data['has_won']:
                return player_id
        return None
    
    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """
        Get the current leaderboard.
        
        Returns:
            List of players sorted by score (highest first)
        """
        players = list(self.players.values())
        players.sort(key=lambda p: (p['score'], -len(p['guesses'])), reverse=True)
        
        leaderboard = []
        for i, player in enumerate(players):
            leaderboard.append({
                'rank': i + 1,
                'player_id': player['id'],
                'player_name': player['name'],
                'score': player['score'],
                'guesses_made': len(player['guesses']),
                'has_won': player['has_won']
            })
        
        return leaderboard 