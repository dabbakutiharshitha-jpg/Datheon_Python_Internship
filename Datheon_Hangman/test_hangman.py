"""
Datheon Python Internship - Hangman Game Automated Test Suite
Verifies all 13 Core Testing Scenarios mandated by project specifications:
1. A new game starts successfully.
2. A random word is selected.
3. Correct guesses reveal letters.
4. Incorrect guesses update the Hangman artwork.
5. Six incorrect guesses trigger game over.
6. Repeated correct guesses do not deduct attempts.
7. Repeated incorrect guesses do not deduct attempts.
8. Numbers and special characters are rejected.
9. Multiple-character input is rejected.
10. Completing the word triggers a winning message.
11. Losing reveals the secret word.
12. New Game resets all previous progress.
13. Refreshing the browser preserves the current game state.
"""

import unittest
import string
from app import app, HANGMAN_STAGES, MAX_INCORRECT_ATTEMPTS, initialize_game, get_game_data, validate_guess, check_win, check_game_over


class HangmanGameTestSuite(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key-123'
        self.client = app.test_client()

    def test_01_new_game_starts_successfully(self):
        """Scenario 1: A new game starts successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("DATHEON PYTHON INTERNSHIP", html)
        self.assertIn("HANGMAN", html)
        self.assertIn("Mistakes Made", html)

    def test_02_random_word_is_selected(self):
        """Scenario 2: A random word is selected from the collection."""
        with self.client:
            self.client.get('/')
            from flask import session
            secret_word = session.get('secret_word')
            self.assertIsNotNone(secret_word)
            self.assertTrue(len(secret_word) >= 3)
            self.assertTrue(secret_word.isalpha())

    def test_03_correct_guesses_reveal_letters(self):
        """Scenario 3: Correct guesses reveal letters."""
        with self.client:
            self.client.get('/')
            from flask import session
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'PYTHON'
                sess['correct_guesses'] = []
                sess['incorrect_guesses'] = []
                sess['game_status'] = 'playing'

            # Guess letter 'P'
            response = self.client.post('/guess', data={'guess': 'P'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            with self.client.session_transaction() as sess:
                self.assertIn('P', sess['correct_guesses'])
                self.assertEqual(len(sess['incorrect_guesses']), 0)

            # Check rendered HTML contains 'P'
            html = response.get_data(as_text=True)
            self.assertIn('P', html)

    def test_04_incorrect_guesses_update_hangman_artwork(self):
        """Scenario 4: Incorrect guesses update the Hangman artwork."""
        with self.client:
            self.client.get('/')
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'FLASK'
                sess['correct_guesses'] = []
                sess['incorrect_guesses'] = []
                sess['game_status'] = 'playing'

            # Stage 0 initially
            with self.client.session_transaction() as sess:
                stage_0_art = HANGMAN_STAGES[len(sess['incorrect_guesses'])]

            # Guess 'Z' (incorrect)
            res = self.client.post('/guess', data={'guess': 'Z'}, follow_redirects=True)
            html = res.get_data(as_text=True)
            
            with self.client.session_transaction() as sess:
                self.assertIn('Z', sess['incorrect_guesses'])
                self.assertEqual(len(sess['incorrect_guesses']), 1)
                stage_1_art = HANGMAN_STAGES[1]

            # Artwork must now reflect Stage 1 (contains head 'O')
            self.assertIn('O', stage_1_art)
            self.assertIn("Stage 1 of 6", html)

    def test_05_six_incorrect_guesses_trigger_game_over(self):
        """Scenario 5: Six incorrect guesses trigger game over."""
        with self.client:
            self.client.get('/')
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'PYTHON'
                sess['correct_guesses'] = []
                sess['incorrect_guesses'] = ['A', 'B', 'C', 'D', 'E']
                sess['game_status'] = 'playing'

            # 6th incorrect guess
            response = self.client.post('/guess', data={'guess': 'F'}, follow_redirects=True)
            html = response.get_data(as_text=True)
            with self.client.session_transaction() as sess:
                self.assertEqual(sess['game_status'], 'lost')
                self.assertEqual(len(sess['incorrect_guesses']), 6)

            self.assertIn("DEFEAT", html)
            self.assertIn("Execution Completed!", html)

    def test_06_repeated_correct_guesses_do_not_deduct_attempts(self):
        """Scenario 6: Repeated correct guesses do not deduct attempts."""
        with self.client:
            self.client.get('/')
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'PYTHON'
                sess['correct_guesses'] = ['P']
                sess['incorrect_guesses'] = []
                sess['game_status'] = 'playing'

            # Guess 'P' again
            response = self.client.post('/guess', data={'guess': 'P'}, follow_redirects=True)
            html = response.get_data(as_text=True)
            with self.client.session_transaction() as sess:
                self.assertEqual(len(sess['incorrect_guesses']), 0)
                self.assertEqual(sess['correct_guesses'].count('P'), 1)
                self.assertEqual(sess['feedback']['type'], 'warning')
            self.assertIn("You already guessed &#39;P&#39;", html)

    def test_07_repeated_incorrect_guesses_do_not_deduct_attempts(self):
        """Scenario 7: Repeated incorrect guesses do not deduct attempts."""
        with self.client:
            self.client.get('/')
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'PYTHON'
                sess['correct_guesses'] = []
                sess['incorrect_guesses'] = ['Z']
                sess['game_status'] = 'playing'

            # Guess 'Z' again
            response = self.client.post('/guess', data={'guess': 'Z'}, follow_redirects=True)
            html = response.get_data(as_text=True)
            with self.client.session_transaction() as sess:
                self.assertEqual(len(sess['incorrect_guesses']), 1)
                self.assertEqual(sess['feedback']['type'], 'warning')
            self.assertIn("You already guessed &#39;Z&#39;", html)

    def test_08_numbers_and_special_characters_are_rejected(self):
        """Scenario 8: Numbers and special characters are rejected."""
        with self.client:
            self.client.get('/')
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'PYTHON'
                sess['correct_guesses'] = []
                sess['incorrect_guesses'] = []
                sess['game_status'] = 'playing'

            # Number guess
            res1 = self.client.post('/guess', data={'guess': '9'}, follow_redirects=True)
            with self.client.session_transaction() as sess:
                self.assertEqual(len(sess['incorrect_guesses']), 0)
                self.assertEqual(len(sess['correct_guesses']), 0)
                self.assertEqual(sess['feedback']['type'], 'danger')

            # Special char guess
            res2 = self.client.post('/guess', data={'guess': '$'}, follow_redirects=True)
            with self.client.session_transaction() as sess:
                self.assertEqual(len(sess['incorrect_guesses']), 0)
                self.assertEqual(len(sess['correct_guesses']), 0)
                self.assertEqual(sess['feedback']['type'], 'danger')

    def test_09_multiple_character_input_is_rejected(self):
        """Scenario 9: Multiple-character input is rejected."""
        with self.client:
            self.client.get('/')
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'PYTHON'
                sess['correct_guesses'] = []
                sess['incorrect_guesses'] = []
                sess['game_status'] = 'playing'

            response = self.client.post('/guess', data={'guess': 'WORD'}, follow_redirects=True)
            with self.client.session_transaction() as sess:
                self.assertEqual(len(sess['incorrect_guesses']), 0)
                self.assertEqual(sess['feedback']['type'], 'danger')
                self.assertIn("Invalid input", sess['feedback']['message'])

    def test_10_completing_word_triggers_winning_message(self):
        """Scenario 10: Completing the word triggers a winning message."""
        with self.client:
            self.client.get('/')
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'CAT'
                sess['correct_guesses'] = ['C', 'A']
                sess['incorrect_guesses'] = []
                sess['game_status'] = 'playing'

            # Guess last letter 'T'
            response = self.client.post('/guess', data={'guess': 'T'}, follow_redirects=True)
            html = response.get_data(as_text=True)
            with self.client.session_transaction() as sess:
                self.assertEqual(sess['game_status'], 'won')
            self.assertIn("VICTORY", html)
            self.assertIn("Congratulations", html)

    def test_11_losing_reveals_secret_word(self):
        """Scenario 11: Losing reveals the secret word."""
        with self.client:
            self.client.get('/')
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'ENCRYPTION'
                sess['correct_guesses'] = []
                sess['incorrect_guesses'] = ['A', 'B', 'C', 'D', 'E']
                sess['game_status'] = 'playing'

            # 6th mistake
            response = self.client.post('/guess', data={'guess': 'F'}, follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertIn("ENCRYPTION", html)
            self.assertIn("The secret word was:", html)

    def test_12_new_game_resets_all_previous_progress(self):
        """Scenario 12: New Game resets all previous progress."""
        with self.client:
            self.client.get('/')
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'PYTHON'
                sess['correct_guesses'] = ['P', 'Y']
                sess['incorrect_guesses'] = ['A', 'B', 'C']
                sess['game_status'] = 'playing'

            # Trigger new game
            response = self.client.post('/new-game', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            with self.client.session_transaction() as sess:
                self.assertEqual(len(sess['correct_guesses']), 0)
                self.assertEqual(len(sess['incorrect_guesses']), 0)
                self.assertEqual(sess['game_status'], 'playing')
                self.assertIn("Fresh game started", sess['feedback']['message'])

    def test_13_refreshing_browser_preserves_game_state(self):
        """Scenario 13: Refreshing the browser preserves the current game state."""
        with self.client:
            self.client.get('/')
            with self.client.session_transaction() as sess:
                sess['secret_word'] = 'ALGORITHM'
                sess['correct_guesses'] = ['A', 'L']
                sess['incorrect_guesses'] = ['Z', 'X']
                sess['game_status'] = 'playing'

            # Simulate refreshing the page (GET /) multiple times
            res1 = self.client.get('/')
            res2 = self.client.get('/')
            self.assertEqual(res1.status_code, 200)
            self.assertEqual(res2.status_code, 200)

            with self.client.session_transaction() as sess:
                self.assertEqual(sess['secret_word'], 'ALGORITHM')
                self.assertEqual(sess['correct_guesses'], ['A', 'L'])
                self.assertEqual(sess['incorrect_guesses'], ['Z', 'X'])
                self.assertEqual(sess['game_status'], 'playing')


if __name__ == '__main__':
    unittest.main()
