"""
Datheon Python Internship - Hangman Game Website
Backend: Python 3 & Flask
Frontend: HTML5 & CSS3 (Zero JavaScript)
Session Management: Flask Sessions
"""

import os
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'datheon-secret-key-hangman-internship-2026-secure')

# Session security configurations
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    MAX_CONTENT_LENGTH=16 * 1024  # Prevent large payloads
)

# 7 Visual ASCII Hangman Stages (Stage 0 to Stage 6)
HANGMAN_STAGES = [
    # Stage 0: 0 mistakes (empty gallows)
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    # Stage 1: 1 mistake (head)
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    # Stage 2: 2 mistakes (head + torso)
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    # Stage 3: 3 mistakes (head + torso + left arm)
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    # Stage 4: 4 mistakes (head + torso + both arms)
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    # Stage 5: 5 mistakes (head + torso + both arms + left leg)
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    # Stage 6: 6 mistakes (head + torso + both arms + both legs)
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
========="""
]

MAX_INCORRECT_ATTEMPTS = 6

# Fallback word list if words.txt is inaccessible
FALLBACK_WORDS = [
    "PYTHON", "FLASK", "DEVELOPER", "INTERNSHIP", "DATHEON",
    "ALGORITHM", "VARIABLE", "FUNCTION", "DATABASE", "FRAMEWORK"
]


def load_words(filepath=None):
    """
    Load clean English words from words.txt.
    Strips whitespace and normalizes to uppercase.
    """
    if filepath is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, 'words.txt')
    
    words = []
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    cleaned = line.strip().upper()
                    if cleaned.isalpha() and len(cleaned) >= 3:
                        words.append(cleaned)
        except Exception as e:
            app.logger.warning(f"Error reading {filepath}: {e}")
    
    return words if words else FALLBACK_WORDS


# Preload word pool once
WORD_POOL = load_words()


def initialize_game():
    """
    Reset and initialize all required game state variables inside Flask session.
    Randomly selects a secret word using random.choice().
    """
    secret_word = random.choice(WORD_POOL)
    session['secret_word'] = secret_word
    session['correct_guesses'] = []
    session['incorrect_guesses'] = []
    session['game_status'] = 'playing'  # 'playing', 'won', 'lost'
    session['feedback'] = {
        'message': "Welcome to Datheon Hangman! Guess a letter to begin.",
        'type': 'info'  # 'info', 'success', 'warning', 'danger'
    }
    session.modified = True


def get_game_data():
    """
    Assemble and return all presentation data needed by the template.
    Ensures safe, consistent state even across page refreshes.
    """
    if 'secret_word' not in session or session.get('game_status') not in ['playing', 'won', 'lost']:
        initialize_game()

    secret_word = session.get('secret_word', '')
    correct_guesses = session.get('correct_guesses', [])
    incorrect_guesses = session.get('incorrect_guesses', [])
    game_status = session.get('game_status', 'playing')
    feedback = session.get('feedback', {'message': '', 'type': 'info'})

    mistakes = len(incorrect_guesses)
    if mistakes > MAX_INCORRECT_ATTEMPTS:
        mistakes = MAX_INCORRECT_ATTEMPTS
    attempts_remaining = max(0, MAX_INCORRECT_ATTEMPTS - mistakes)

    # Build letter slots for hidden word display
    word_display = []
    for char in secret_word:
        if char in correct_guesses or game_status in ['won', 'lost']:
            word_display.append({
                'char': char,
                'revealed': True,
                'missed': (game_status == 'lost' and char not in correct_guesses)
            })
        else:
            word_display.append({
                'char': '_',
                'revealed': False,
                'missed': False
            })

    # Build A-Z alphabet status for visual tracking and keyboard
    alphabet_status = []
    for letter in string.ascii_uppercase:
        if letter in correct_guesses:
            status = 'correct'
        elif letter in incorrect_guesses:
            status = 'incorrect'
        else:
            status = 'available'
        alphabet_status.append({'letter': letter, 'status': status})

    current_stage_art = HANGMAN_STAGES[mistakes]

    return {
        'secret_word': secret_word,
        'word_display': word_display,
        'correct_guesses': sorted(correct_guesses),
        'incorrect_guesses': sorted(incorrect_guesses),
        'all_guesses': sorted(correct_guesses + incorrect_guesses),
        'mistakes': mistakes,
        'max_mistakes': MAX_INCORRECT_ATTEMPTS,
        'attempts_remaining': attempts_remaining,
        'current_stage_art': current_stage_art,
        'game_status': game_status,
        'feedback': feedback,
        'alphabet_status': alphabet_status
    }


def validate_guess(guess_raw, all_guessed):
    """
    Validates user input according to strict security & game rules:
    - Must not be empty.
    - Must be exactly 1 character.
    - Must be an alphabetic letter (A-Z).
    - Checks for duplicate guesses without penalty.

    Returns:
        (is_valid_format: bool, letter_or_none: str, error_type: str, message: str)
    """
    if not guess_raw:
        return False, None, 'empty', "Please enter a letter before submitting."

    cleaned = guess_raw.strip().upper()

    if len(cleaned) != 1:
        return False, None, 'length', "Invalid input: Please enter exactly one letter at a time."

    if not cleaned.isalpha() or cleaned not in string.ascii_uppercase:
        return False, None, 'not_alpha', f"Invalid character '{cleaned}': Only alphabetic letters (A-Z) are accepted."

    if cleaned in all_guessed:
        return False, cleaned, 'duplicate', f"You already guessed '{cleaned}'. Try a different letter!"

    return True, cleaned, None, None


def check_win(secret_word, correct_guesses):
    """
    Determine if the player has guessed all letters in the secret word.
    """
    return all(char in correct_guesses for char in secret_word)


def check_game_over(incorrect_count):
    """
    Determine if the maximum number of incorrect attempts (6) has been reached.
    """
    return incorrect_count >= MAX_INCORRECT_ATTEMPTS


def process_guess(guess_raw):
    """
    Executes the full game loop logic for a single guess.
    Updates session state safely and generates appropriate feedback messages.
    """
    if session.get('game_status') != 'playing':
        session['feedback'] = {
            'message': "Game is already finished! Click 'New Game' to play again.",
            'type': 'warning'
        }
        session.modified = True
        return

    secret_word = session.get('secret_word', '')
    correct_guesses = session.get('correct_guesses', [])
    incorrect_guesses = session.get('incorrect_guesses', [])
    all_guessed = set(correct_guesses + incorrect_guesses)

    # Validate input
    is_valid, letter, err_type, err_msg = validate_guess(guess_raw, all_guessed)

    if not is_valid:
        if err_type == 'duplicate':
            # Duplicate guess: Do NOT deduct attempt, show warning
            session['feedback'] = {
                'message': err_msg,
                'type': 'warning'
            }
        else:
            # Syntax / format validation error: Do NOT deduct attempt
            session['feedback'] = {
                'message': err_msg,
                'type': 'danger'
            }
        session.modified = True
        return

    # Process valid new letter
    if letter in secret_word:
        correct_guesses.append(letter)
        session['correct_guesses'] = correct_guesses

        if check_win(secret_word, correct_guesses):
            session['game_status'] = 'won'
            session['feedback'] = {
                'message': f"🎉 Spectacular Victory! You successfully decoded '{secret_word}'!",
                'type': 'success'
            }
        else:
            session['feedback'] = {
                'message': f"🎯 Brilliant! '{letter}' is part of the secret word.",
                'type': 'success'
            }
    else:
        incorrect_guesses.append(letter)
        session['incorrect_guesses'] = incorrect_guesses

        if check_game_over(len(incorrect_guesses)):
            session['game_status'] = 'lost'
            session['feedback'] = {
                'message': f"💀 Game Over! You ran out of attempts. The secret word was '{secret_word}'.",
                'type': 'danger'
            }
        else:
            remaining = MAX_INCORRECT_ATTEMPTS - len(incorrect_guesses)
            session['feedback'] = {
                'message': f"❌ Miss! '{letter}' is not in the word. ({remaining} attempt{'s' if remaining != 1 else ''} left)",
                'type': 'danger'
            }

    session.modified = True


# ==========================================
# FLASK APPLICATION ROUTES (Pure HTML/CSS)
# ==========================================

@app.route('/', methods=['GET'])
def index():
    """
    Main game view. Renders the full game board with current session data.
    Preserves state across refreshes without resubmission prompts.
    """
    game_data = get_game_data()
    return render_template('index.html', **game_data)


@app.route('/guess', methods=['POST'])
def guess():
    """
    Handles guess submission via standard HTML form POST.
    Redirects back to index (Post/Redirect/Get pattern) for seamless UX without JS.
    """
    user_guess = request.form.get('guess', '')
    process_guess(user_guess)
    return redirect(url_for('index'))


@app.route('/new-game', methods=['POST', 'GET'])
def new_game():
    """
    Resets the session game state and picks a new random word.
    """
    initialize_game()
    session['feedback'] = {
        'message': "Fresh game started! Good luck with your new secret word.",
        'type': 'info'
    }
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))


@app.errorhandler(500)
def server_error(e):
    initialize_game()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Local development server
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Datheon Hangman Game on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
