# src/game/gui.py
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from pathlib import Path
import sys



class GameWindow(QMainWindow):
    """Main game window."""
    
    def __init__(self):
        super().__init__()
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
       

def main():
    """Launch the game GUI."""
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()