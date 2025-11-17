import random 
class WordGame:
    def __init__(self, min_len=3, max_len=6, attempts=6):
        self.min_len =min_len
        self.max_len = max_len
        self.attempts = attempts
        self.attempts_left = attempts
        self.guessed_letters = set()
        self.word = ""
        self.load_words()
    def load_words(self):
        self.words = []
        with open("words_alpha.txt", "r", encoding="utf-8") as f:
            for w in f:
                w=w.strip().lower()
                if w.isalpha and self.min_len<= len(w) <= self.max_len:
                    self.words.append(w)
    def start_new_game(self):
        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.attempts_left = self.attempts
    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return "already"
        self.guessed_letters.add(letter)
        if letter in self.word:
            if all(c in self.guessed_letters for c in self.word):
                return "win"
            return "correct"
        else:
            self.attempts_left -=1
            if self.attempts_left ==0:
                return "lose"
            return "wrong"
    def get_display_word(self):
        return " ".join([c if c in self.guessed_letters else "_" for c in self.word])
