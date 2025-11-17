import random
import sys
WORDS_FILE = "words_alpha.txt"
def load_words(min_len=3, max_len=12):
    words =[]
    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        for w in f:
            w=w.strip().lower()
            if not w.isalpha():
                continue
            if len(w) < min_len or len(w)>max_len:
                continue
            words.append(w)
    return words
def choose_word(words):
    return random.choice(words)
def play_game():
    print("choose difficulty: 1) Easy 2) Medium 3) Hard")
    choice = input("Difficulty (1/2/3): ").strip()
    if choice =="1":
        min_len, max_len, attempts =3,6,8
    elif choice =="3":
        min_len, max_len, attempts =8,20,4
    else:
        min_len, max_len, attempts =5,10,6
    print(f"Loading words (length{min_len}-{max_len}) - this may take a second...")
    words = load_words(min_len=min_len, max_len=max_len)
    if not words:
        print("No words found with those constraints. Exiting.")
        sys.exit(1)
    word = choose_word(words)
    guessed_letters = set()
    attempts_left = attempts
    print("\n Welcome to the world of guessing Game!")
    while attempts_left > 0 :
        display = "".join([c if c in guessed_letters else "_" for c in word])
        print("\nWord:", display, "Attempts left:", attempts_left)
        guess = input("Guess a letter: ").lower().strip()
        if len(guess)!= 1 or not guess.isalpha():
            print("Entera asingle letter.")
            continue
        if guess in guessed_letters:
            print("Already guessed.")
            continue
        guessed_letters.add(guess)
        if guess in word:
            print("Good!")
            if all(ch in guessed_letters for ch in word):
                print("You won! Word: ", word)
                return 
        else:
            attempts_left -=1
            print("Wrong!")
    print("Game over. Word was:", word)
if __name__ == "__main__":
    play_game()

