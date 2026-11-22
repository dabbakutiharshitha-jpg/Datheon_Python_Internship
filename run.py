"""
Datheon Python Internship - Root Convenience Launcher
Runs the Hangman Flask Application from Datheon_Hangman/app.py
"""
import sys
import os

# Add Datheon_Hangman directory to sys.path
base_dir = os.path.dirname(os.path.abspath(__file__))
hangman_dir = os.path.join(base_dir, 'Datheon_Hangman')
sys.path.insert(0, hangman_dir)

from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Datheon Hangman Game running at: http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
