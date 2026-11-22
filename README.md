# 🎯 Datheon Python Internship – Hangman Game Website

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.x-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3-orange.svg?logo=html5&logoColor=white)](https://developer.mozilla.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Zero%20(Pure%20Python)-brightgreen.svg)](#technology-stack)
[![Tests](https://img.shields.io/badge/Tests-13%2F13%20Passed-success.svg)](#testing-and-verification)

A modern, responsive, server-driven **Hangman Word Guessing Game Website** built for the **Datheon Python Internship**.

This project implements a fully interactive browser game adhering to a strict **Zero-JavaScript** requirement: 100% of game state, validations, random selection, and outcome evaluations are executed on the Python backend using **Flask sessions**, while HTML5 and CSS3 deliver a cyber-indigo dashboard interface.

---

## 🌟 Key Features

- **Pure Python Backend Logic**: Complete game loop implemented strictly in Python using modular functions.
- **Strict Zero JavaScript**: No JS libraries, frameworks, scripts, or inline event handlers. All interactions are handled via standard HTTP POST and the Post/Redirect/Get pattern.
- **Dynamic ASCII Gallows Artwork**: 7 visual stages (Stage 0: Empty Gallows through Stage 6: Full Hangman) rendered in a retro-modern monospace terminal viewer.
- **Word Pool & Random Selection**: Loads curated English vocabulary from `words.txt` and randomly selects words using Python's `random.choice()`. Includes graceful fallback protection.
- **State Preservation Across Refreshes**: Uses secure Flask sessions (`SESSION_COOKIE_HTTPONLY=True`, `SameSite=Lax`). Refreshing the browser does not reset progress or prompt for form resubmission.
- **Duplicate Guess Protection**: Entering a previously guessed letter displays a friendly warning and never deducts an attempt.
- **Separate Guess Tracking**: Displays correctly guessed and incorrectly guessed letters in distinct, color-coded badges.
- **Interactive Pure-HTML Virtual Keypad**: An on-screen A-Z keyboard built entirely with HTML submit buttons. Provides an intuitive click-to-guess interface on desktop and mobile without a single line of JS.
- **Strict Backend Validation**: Sanitizes and validates all incoming data, rejecting empty inputs, multi-character strings, numbers, and symbols.
- **Game-Over & Victory Screens**: Automatic detection of win/loss conditions. Winning congratulates the player; losing reveals the secret word. Subsequent guesses are disabled once the game concludes.
- **Responsive Cyber-Indigo UI/UX**: Custom CSS3 design with dark navy backgrounds, purple and indigo gradients, glassmorphism cards, glowing status pills, and responsive layouts across desktops, tablets, and phones.

---

## 🛠️ Technology Stack

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Backend** | Python 3 | Python 3.10+ / 3.14 compatible |
| **Web Framework** | Flask | Lightweight WSGI web application framework |
| **Template Engine** | Jinja2 | Server-side templating and condition evaluation |
| **Frontend Structure** | HTML5 | Clean semantic HTML forms, badges, and layout |
| **Frontend Styling** | CSS3 | Responsive flexbox/grid, glassmorphism, glowing shadows |
| **State Management** | Flask Sessions | Secure encrypted client-side session cookies |
| **Client-Side Scripts** | **None (Zero JS)** | Strictly excluded by project specifications |

---

## 📂 Project Directory Structure

```text
Datheon_Hangman/
│
├── app.py                 # Core Flask backend, game logic, routes & session handling
├── words.txt              # Curated dictionary of 250+ English vocabulary words
├── requirements.txt       # Python dependencies (Flask, Werkzeug, Jinja2)
├── test_hangman.py        # Automated test suite covering all 13 test scenarios
├── README.md              # Project documentation and setup guide
│
├── templates/
│   └── index.html         # Jinja2 HTML5 interface (zero JavaScript)
│
└── static/
    └── style.css          # Premium responsive dark navy CSS3 styling
```

---

## 🚀 Installation & Setup Instructions

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system. Check your version:
```bash
python --version
```

### 2. Clone or Navigate to the Repository
```bash
cd Datheon_python_Internship/Datheon_Hangman
```

### 3. Create a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🎮 How to Run the Application

Start the local Flask development server:

```bash
python app.py
```

Once running, open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📜 Game Rules

1. **Objective**: Guess the secret hidden English word one letter at a time before the gallows is completed.
2. **Hidden Word**: The word is represented by blank underscores representing each character.
3. **Guessing**:
   - Type a single letter (A–Z) into the input box and click **Submit Guess**, OR
   - Click any available letter on the on-screen **Virtual Keypad**.
4. **Attempts**: You have a maximum of **6 incorrect attempts**.
5. **Penalties**:
   - Correct guesses reveal the letter in all matching positions (no penalty).
   - Incorrect guesses advance the Hangman ASCII gallows by 1 stage and deduct 1 attempt.
   - Repeated guesses (whether correct or incorrect) show a warning and do **not** deduct attempts.
   - Invalid characters (numbers, punctuation, multiple letters) are rejected without penalty.
6. **Winning**: Successfully reveal all letters before reaching 6 mistakes.
7. **Losing**: Making 6 incorrect guesses assembles the full hangman and ends the game. The hidden word is revealed.
8. **Reset**: Click **New Game** at any time to start a fresh round with a newly randomized word.

---

## 🧪 Testing and Verification

The project includes an automated test suite verifying all 13 required scenarios:

```bash
python -m unittest test_hangman.py -v
```

### Test Results Summary:
```text
test_01_new_game_starts_successfully (test_hangman.HangmanGameTestSuite) ... ok
test_02_random_word_is_selected (test_hangman.HangmanGameTestSuite) ... ok
test_03_correct_guesses_reveal_letters (test_hangman.HangmanGameTestSuite) ... ok
test_04_incorrect_guesses_update_hangman_artwork (test_hangman.HangmanGameTestSuite) ... ok
test_05_six_incorrect_guesses_trigger_game_over (test_hangman.HangmanGameTestSuite) ... ok
test_06_repeated_correct_guesses_do_not_deduct_attempts (test_hangman.HangmanGameTestSuite) ... ok
test_07_repeated_incorrect_guesses_do_not_deduct_attempts (test_hangman.HangmanGameTestSuite) ... ok
test_08_numbers_and_special_characters_are_rejected (test_hangman.HangmanGameTestSuite) ... ok
test_09_multiple_character_input_is_rejected (test_hangman.HangmanGameTestSuite) ... ok
test_10_completing_word_triggers_winning_message (test_hangman.HangmanGameTestSuite) ... ok
test_11_losing_reveals_secret_word (test_hangman.HangmanGameTestSuite) ... ok
test_12_new_game_resets_all_previous_progress (test_hangman.HangmanGameTestSuite) ... ok
test_13_refreshing_browser_preserves_game_state (test_hangman.HangmanGameTestSuite) ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.224s

OK
```

---

## 🔒 Security & Robustness Highlights

- **Backend Validation**: Never trusts the frontend; all submissions are checked for type, length, character set, and duplication in Python.
- **Session Protection**: Uses standard cryptographically signed Flask session cookies with `HTTPOnly` and `SameSite` flags.
- **Post/Redirect/Get Pattern**: Prevents duplicate form submissions when users press F5 / reload.
- **Secret Word Concealment**: The secret word is kept on the server and is never exposed in the HTML markup or client-side storage until the game has concluded in a loss.

---

## 📤 Instructions for Uploading to GitHub

To push this project to your GitHub repository:

```bash
# 1. Initialize git in the project root
git init

# 2. Add all project files
git add .

# 3. Commit the changes
git commit -m "Complete Datheon Python Internship Hangman Game Website"

# 4. Rename main branch
git branch -M main

# 5. Add your GitHub remote repository URL
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# 6. Push to GitHub
git push -u origin main
```

---

## 👨‍💻 Internship Attribution

- **Program**: Datheon Python Internship
- **Project**: Interactive Hangman Web Application
- **Author**: Internship Candidate
- **Technology**: Python 3 • Flask • Jinja2 • HTML5 • CSS3 (Zero JavaScript)
