# Liam Whitehead
# CIS256 Spring 2026
# Exercise Assignment 4

import pytest

# Import the functions we want to test from our game module
from guess_the_word import (
    WORD_LIST,
    get_random_word,
    build_display,
    is_word_guessed,
    process_guess,
)


# ─────────────────────────────────────────────────────────────────────────────
# Tests for get_random_word()
# ─────────────────────────────────────────────────────────────────────────────

class TestGetRandomWord:
    """Tests ensuring a word is selected correctly from the predefined list."""

    def test_word_comes_from_word_list(self):
        """The returned word must be an element of WORD_LIST."""
        word = get_random_word()
        assert word in WORD_LIST, (
            f"'{word}' was not found in WORD_LIST"
        )

    def test_word_is_a_string(self):
        """get_random_word() should always return a string."""
        assert isinstance(get_random_word(), str)

    def test_word_is_not_empty(self):
        """The returned word should never be an empty string."""
        assert len(get_random_word()) > 0

    def test_custom_word_list(self):
        """get_random_word() should respect a custom list passed as argument."""
        custom_list = ["apple", "banana", "cherry"]
        word = get_random_word(custom_list)
        assert word in custom_list

    def test_single_word_list_always_returns_that_word(self):
        """When the list has one item, that item must always be returned."""
        assert get_random_word(["only"]) == "only"


# ─────────────────────────────────────────────────────────────────────────────
# Tests for process_guess()
# ─────────────────────────────────────────────────────────────────────────────

class TestProcessGuess:
    """Tests verifying that individual letter guesses are handled correctly."""

    # ── Correct guesses ───────────────────────────────────────────────────

    def test_correct_guess_is_valid(self):
        """A letter that is in the word should be marked valid and correct."""
        guessed = set()
        valid, already, correct = process_guess("p", "python", guessed)
        assert valid is True
        assert already is False
        assert correct is True

    def test_correct_guess_added_to_guessed_set(self):
        """After a correct guess the letter should appear in guessed_letters."""
        guessed = set()
        process_guess("p", "python", guessed)
        assert "p" in guessed

    def test_correct_guess_case_insensitive(self):
        """Uppercase input should be treated the same as lowercase."""
        guessed = set()
        valid, already, correct = process_guess("P", "python", guessed)
        assert valid is True
        assert correct is True
        # Stored in lowercase
        assert "p" in guessed

    # ── Incorrect guesses ─────────────────────────────────────────────────

    def test_incorrect_guess_is_valid_but_wrong(self):
        """A letter not in the word should still be valid, but not correct."""
        guessed = set()
        valid, already, correct = process_guess("z", "python", guessed)
        assert valid is True
        assert already is False
        assert correct is False

    def test_incorrect_guess_still_added_to_guessed_set(self):
        """A wrong letter should still be recorded so it can't be reused."""
        guessed = set()
        process_guess("z", "python", guessed)
        assert "z" in guessed

    # ── Already-guessed letter ────────────────────────────────────────────

    def test_already_guessed_letter_detected(self):
        """Guessing the same letter twice should be flagged."""
        guessed = {"p"}
        valid, already, correct = process_guess("p", "python", guessed)
        assert valid is True
        assert already is True

    def test_already_guessed_does_not_duplicate_in_set(self):
        """The guessed set should not grow when the same letter is re-entered."""
        guessed = {"p"}
        process_guess("p", "python", guessed)
        # Sets automatically de-duplicate, but size should remain 1
        assert guessed == {"p"}

    # ── Invalid inputs ────────────────────────────────────────────────────

    def test_non_alpha_input_is_invalid(self):
        """Digits and symbols should be rejected as invalid input."""
        guessed = set()
        valid, _, _ = process_guess("3", "python", guessed)
        assert valid is False

    def test_empty_string_is_invalid(self):
        """An empty string should be rejected."""
        guessed = set()
        valid, _, _ = process_guess("", "python", guessed)
        assert valid is False

    def test_multi_character_input_is_invalid(self):
        """Entering more than one character should be rejected."""
        guessed = set()
        valid, _, _ = process_guess("py", "python", guessed)
        assert valid is False

    def test_space_is_invalid(self):
        """A space character should be rejected."""
        guessed = set()
        valid, _, _ = process_guess(" ", "python", guessed)
        assert valid is False


# ─────────────────────────────────────────────────────────────────────────────
# Tests for build_display()
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildDisplay:
    """Tests for the function that renders the current word state."""

    def test_no_guesses_shows_all_blanks(self):
        """With no guesses, every character should show as an underscore."""
        display = build_display("cat", set())
        assert display == "_ _ _"

    def test_correct_guess_revealed(self):
        """A guessed letter should appear in its correct position(s)."""
        display = build_display("cat", {"c"})
        assert display == "c _ _"

    def test_all_letters_guessed_shows_word(self):
        """When every letter is guessed the display should match the word."""
        display = build_display("cat", {"c", "a", "t"})
        assert display == "c a t"

    def test_repeated_letter_revealed_everywhere(self):
        """Guessing a letter that appears multiple times reveals all copies."""
        display = build_display("balloon", {"l"})
        # 'l' appears at indices 2 and 3
        assert display == "_ _ l l _ _ _"


# ─────────────────────────────────────────────────────────────────────────────
# Tests for is_word_guessed()
# ─────────────────────────────────────────────────────────────────────────────

class TestIsWordGuessed:
    """Tests checking whether the win condition is detected correctly."""

    def test_word_not_guessed_when_empty(self):
        """No guesses means the word is definitely not complete."""
        assert is_word_guessed("cat", set()) is False

    def test_word_not_guessed_partially(self):
        """Partial guesses should not trigger the win condition."""
        assert is_word_guessed("cat", {"c", "a"}) is False

    def test_word_guessed_exactly(self):
        """Supplying exactly the right letters should return True."""
        assert is_word_guessed("cat", {"c", "a", "t"}) is True

    def test_word_guessed_with_extra_letters(self):
        """Extra wrong guesses in the set should not prevent a win."""
        assert is_word_guessed("cat", {"c", "a", "t", "z", "x"}) is True
