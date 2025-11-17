import sys
from PyQt5.QtWidgets import(
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QStackedWidget, QHBoxLayout
)
from game_logic import WordGame
class HomeScreen(QWidget):
    def __init__(self, app_manager):
        super().__init__()
        self.app_manager = app_manager
        layout = QVBoxLayout()
        title = QLabel("WORD GUESSING GAME")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        layout.addWidget(title)

        btn_easy = QPushButton("Easy (3–6 letters)")
        btn_medium = QPushButton("Medium (5–10 letters)")
        btn_hard = QPushButton("Hard (8–20 letters)")

        btn_easy.clicked.connect(lambda: self.app_manager.start_game(3, 6, 8))
        btn_medium.clicked.connect(lambda: self.app_manager.start_game(5, 10, 6))
        btn_hard.clicked.connect(lambda: self.app_manager.start_game(8, 20, 4))

        layout.addWidget(btn_easy)
        layout.addWidget(btn_medium)
        layout.addWidget(btn_hard)

        self.setLayout(layout)
class GameScreen(QWidget):
    def __init__(self, app_manager):
        super().__init__()
        self.app_manager = app_manager

        self.layout = QVBoxLayout()

        self.word_label = QLabel("_ _ _")
        self.word_label.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(self.word_label)

        self.info_label = QLabel("")
        self.layout.addWidget(self.info_label)

        self.attempts_label = QLabel("Attempts left: 0")
        self.layout.addWidget(self.attempts_label)

        self.input_box = QLineEdit()
        self.input_box.setMaxLength(1)
        self.layout.addWidget(self.input_box)

        btn_guess = QPushButton("Guess")
        btn_guess.clicked.connect(self.make_guess)
        self.layout.addWidget(btn_guess)

        btn_home = QPushButton("Back to Home")
        btn_home.clicked.connect(self.app_manager.go_home)
        self.layout.addWidget(btn_home)

        self.setLayout(self.layout)

    def update_display(self):
        self.word_label.setText(self.app_manager.game.get_display_word())
        self.attempts_label.setText(f"Attempts left: {self.app_manager.game.attempts_left}")

    def make_guess(self):
        letter = self.input_box.text().strip().lower()
        self.input_box.clear()

        if not letter.isalpha() or len(letter) != 1:
            self.info_label.setText("Enter a single letter.")
            return

        result = self.app_manager.game.guess_letter(letter)

        if result == "correct":
            self.info_label.setText("Good!")
        elif result == "wrong":
            self.info_label.setText("Wrong!")
        elif result == "already":
            self.info_label.setText("Already guessed.")
        elif result == "win":
            QMessageBox.information(self, "Victory!", "You WON!")
            self.app_manager.go_home()
            return
        elif result == "lose":
            QMessageBox.information(self, "Game Over", f"You lost! Word was: {self.app_manager.game.word}")
            self.app_manager.go_home()
            return

        self.update_display()


class AppManager:
    def __init__(self):
        self.stack = QStackedWidget()

        self.home = HomeScreen(self)
        self.game_screen = GameScreen(self)

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.game_screen)

        self.stack.setCurrentWidget(self.home)

    def start_game(self, min_len, max_len, attempts):
        self.game = WordGame(min_len, max_len, attempts)
        self.game.start_new_game()
        self.game_screen.update_display()
        self.stack.setCurrentWidget(self.game_screen)

    def go_home(self):
        self.stack.setCurrentWidget(self.home)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = AppManager()
    manager.stack.setWindowTitle("Word Guessing Game")
    manager.stack.resize(400, 300)
    manager.stack.show()
    sys.exit(app.exec_())