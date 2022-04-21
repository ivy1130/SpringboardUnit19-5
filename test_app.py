from app import app
from unittest import TestCase
from flask import session
from boggle import Boggle

class BoggleTestCase(TestCase):
    def test_boggle_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Click here to begin!', html)

# How to test javascript? When user is on the home page, they need to click a button to actually start and go to another html.

    def test_boggle_start_game(self):
        with app.test_client() as client:
            res = client.get('/start-game')
            html = res.get_data(as_text=True)

            self.assertIn('current_game', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('play_count'))
            self.assertIn(b'High Score:', res.data)
            self.assertIn(b'Input your guess here:', res.data)

    def test_boggle_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['current_game'] = [["C", "A", "T", "T", "T"], 
                                        ["C", "A", "T", "T", "T"], 
                                        ["C", "A", "T", "T", "T"], 
                                        ["C", "A", "T", "T", "T"], 
                                        ["C", "A", "T", "T", "T"]]
                
        res = client.get('/check-guess?guess=cat')
        self.assertEqual(res.json['result'], 'ok')

    def test_boggle_word_not_on_board(self):
        with app.test_client() as client:
            client.get('/start-game')
            res = client.get('/check-guess?guess=hello')
            self.assertEqual(res.json['result'], 'not-on-board')


    def test_boggle_invalid_word(self):
        with app.test_client() as client:
            client.get('/start-game')
            res = client.get('/check-guess?guess=dasfrxf')
            self.assertEqual(res.json['result'], 'not-word')
        
# How can I check the javascript to see if the DOM has updated with the proper message?

    def test_boggle_stats(self):
        with app.test_client() as client:
            client.post('/add-score', json={'score': 20})
            self.assertEqual(session['play_count'], 1)
            self.assertEqual(session['highscore'], 20)
