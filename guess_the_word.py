# Liam Whitehead
# CIS256 Spring 2026
# Exercise Assignment 4

import random

# ─── Predefined word list ───────────────────────────────────────────────────
WORD_LIST = [
    "python", "hangman", "keyboard", "program", "library",
    "function", "variable", "loop", "string", "integer",
    "boolean", "dictionary", "list", "tuple", "module",
    "class", "object", "method", "import", "exception"
]

# Maximum number of incorrect guesses allowed before the game ends
MAX_ATTEMPTS = 6


def get_random_word(word_list=WORD_LIST):
    """Select and return a random word from the provided word list."""
    return random.choice(word_list)


def build_display(secret_word, guessed_letters):
    """
    Build the current display string showing correctly guessed letters
    and underscores for letters not yet guessed.

    Parameters:
        secret_word (str): The word to be guessed.
        guessed_letters (set): Letters the player has already guessed.

    Returns:
        str: A string like '_ y _ h o n' for partially guessed words.
    """
    return " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )


def is_word_guessed(secret_word, guessed_letters):
    """
    Check whether every letter in the secret word has been guessed.

    Parameters:
        secret_word (str): The word to be guessed.
        guessed_letters (set): Letters guessed so far.

    Returns:
        bool: True if all letters have been guessed, False otherwise.
    """
    return all(letter in guessed_letters for letter in secret_word)


def process_guess(guess, secret_word, guessed_letters):
    """
    Validate and process a single letter guess.

    Parameters:
        guess (str): The player's input.
        secret_word (str): The word to be guessed.
        guessed_letters (set): Letters guessed so far (modified in place).

    Returns:
        tuple: (valid, already_guessed, correct)
            valid          – True if guess was a single alphabetic character.
            already_guessed – True if the letter was guessed before.
            correct         – True if the letter is in the secret word.
    """
    # Ensure the input is exactly one letter
    if len(guess) != 1 or not guess.isalpha():
        return False, False, False

    guess = guess.lower()

    # Check whether this letter was already submitted
    if guess in guessed_letters:
        return True, True, False

    # Add the new guess to the running set
    guessed_letters.add(guess)

    # Determine whether the guess is correct
    correct = guess in secret_word
    return True, False, correct


def play_game():
    """
    Main game loop. Handles all input/output for one full round of
    Guess the Word (a Hangman-style game).
    """
    print("\n" + "=" * 40)
    print("   WELCOME TO GUESS THE WORD!")
    print("=" * 40)

    # Pick a random secret word from the list
    secret_word = get_random_word()

    # Track all letters the player has guessed
    guessed_letters = set()

    # Count wrong guesses; game ends when this reaches MAX_ATTEMPTS
    wrong_guesses = 0

    print(f"\nThe word has {len(secret_word)} letters.")
    print(f"You have {MAX_ATTEMPTS} incorrect guesses allowed.\n")

    # ── Game loop ──────────────────────────────────────────────────────────
    while wrong_guesses < MAX_ATTEMPTS:

        # Show current progress and remaining attempts
        print("Word: ", build_display(secret_word, guessed_letters))
        print(f"Incorrect guesses left: {MAX_ATTEMPTS - wrong_guesses}")

        # Show letters already tried (sorted for readability)
        if guessed_letters:
            print("Letters guessed: ", ", ".join(sorted(guessed_letters)))

        # Prompt the player for their next guess
        guess = input("\nGuess a letter: ").strip().lower()

        # ── Validate the input ─────────────────────────────────────────────
        valid, already_guessed, correct = process_guess(
            guess, secret_word, guessed_letters
        )

        if not valid:
            print("⚠  Please enter a single letter (a–z).")
            continue

        if already_guessed:
            print(f"  You already guessed '{guess}'. Try a different letter.")
            continue

        # ── React to the guess result ──────────────────────────────────────
        if correct:
            print(f"  ✓ Great! '{guess}' is in the word.")
        else:
            wrong_guesses += 1
            print(f"  ✗ '{guess}' is not in the word. "
                  f"({MAX_ATTEMPTS - wrong_guesses} guesses left)")

        # ── Check for win ──────────────────────────────────────────────────
        if is_word_guessed(secret_word, guessed_letters):
            print("\n" + "=" * 40)
            print(f"  🎉 CONGRATULATIONS! You guessed the word: '{secret_word}'!")
            print("=" * 40 + "\n")
            return True   # Player won

        print()  # blank line for readability

    # ── Player ran out of attempts ─────────────────────────────────────────
    print("\n" + "=" * 40)
    print(f"  Game over! The word was: '{secret_word}'.")
    print("=" * 40 + "\n")
    return False   # Player lost


# ─── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Allow the player to play multiple rounds
    while True:
        play_game()
        again = input("Play again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Thanks for playing!")
            break
