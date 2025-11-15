# src/game/gui.py
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from pathlib import Path
import sys

from .card_loader import get_card_image_path
from .state import GameState



class GameWindow(QMainWindow):
    """Main game window."""
    
    def __init__(self, game_state: GameState, cards_dir: Path):
        super().__init__()
        self.game_state = game_state
        self.cards_dir = cards_dir
        
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("SpotiCards Game")
        self.setGeometry(100, 100, 1200, 800)  # x, y, width, height
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Placeholder label
        label = QLabel("Game will go here!")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

    def display_card(self, card_image_path: Path):
        """
        Display the card image in the GUI.
        """
        pass
       

def main(tracks: list[dict], cards_dir: Path):
    """
    Launch the game GUI.

    Args:
        tracks: List of playlist track metadata dictionaries
        cards_dir: Path to directory containing cards
    """
    app = QApplication(sys.argv)

    # Create game state
    game_state = GameState(tracks, target_cards=10)

    # Create game window
    window = GameWindow(game_state, cards_dir)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()