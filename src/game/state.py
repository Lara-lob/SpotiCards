# src/game/state.py
from dataclasses import dataclass
import random

@dataclass
class CardGuess:
    title: str = ""
    artist: str = ""


class GameState:
    """
    Manages the state of a single game session.
    
    Responsibilities:
    - Track which cards have been played/remain
    - Store the timeline of placed cards
    - Track current card being guessed
    - Keep score and progress
    """
    def __init__(self, tracks: list[dict], target_cards: int = 10):
        """
        Initialize the game state.
        Args:
            tracks (list[dict]): List of track metadata dictionaries
            target_cards (int): Number of correctly placed cards needed to win
        """
        # Game configuration
        self.target_cards = target_cards
        
        # Card pools
        self.remaining_cards = tracks.copy()  # Cards not yet drawn
        random.shuffle(self.remaining_cards)
        self.timeline = []  # Cards placed in order (chronologically)
        
        # Current card state
        self.current_card: dict | None = None
        self.current_guess = CardGuess()
        
        # Score tracking
        self.bonus_points = 0
        self.cards_placed_correctly = 0
        
        # Game status
        self.is_won = False

    def draw_next_card(self) -> dict | None:
        """
        Draw the next card from the remaining pool.
        Returns:
            dict | None: The next track metadata dictionary, or None if no cards left
        """
        if not self.remaining_cards:
            return None
        self.current_card = self.remaining_cards.pop()
        self.current_guess = CardGuess()  # Reset guess
        return self.current_card
    
    def place_current_card(self, position: int) -> bool:
        """
        Place the current card in the timeline at the specified position.  
        Args:
            position (int): Index in the timeline to place the current card
        Returns:
            bool: True if placed correctly, False otherwise
        """
        if self.current_card is None:
            raise ValueError("No current card to place.")
        
        # Insert the current card into the timeline at the specified position
        self.timeline.insert(position, self.current_card)
        
        # Check if placed correctly (chronological order)
        is_correct = self._is_placement_correct(position)
        if is_correct:
            self.cards_placed_correctly += 1
            if self.cards_placed_correctly >= self.target_cards:
                self.is_won = True
        
        # Clear current card
        self.current_card = None
        
        return is_correct
    
    def _is_placement_correct(self, position: int) -> bool:
        """
        Check if the card placed at the given position is in correct chronological order.
        Args:
            position (int): Index in the timeline where the card was placed
        Returns:
            bool: True if the placement is correct, False otherwise
        """
        current_year = self.timeline[position]["release_year"]

        if position > 0:
            left_year = self.timeline[position-1]
            if current_year < left_year:
                return False
            
        if position < len(self.timeline) - 1:
            right_year = self.timeline[position+1]["release_year"]
            if current_year > right_year:
                return False
            
        return True
    
    def check_guess(self) -> bool:
        """
        Check if the current guess matches the current card's metadata.
        Returns:
            bool: True if the guess is correct, False otherwise
        """
        # TODO: Implement fuzzy matching for partial correctness
        if self.current_card is None:
            raise ValueError("No current card to check guess against.")
        
        is_title_correct = (
            self.current_guess.title.lower().strip() == 
            self.current_card["name_cleaned"].lower().strip()
        )
        is_artist_correct = (
            self.current_guess.artist.lower().strip() == 
            self.current_card["artists"].lower().strip()
        )
        
        return is_title_correct and is_artist_correct
    
    def add_bonus_points(self, points: int) -> None:
        """
        Add bonus points to the player's score.
        Args:
            points (int): Number of bonus points to add
        """
        self.bonus_points += points
        