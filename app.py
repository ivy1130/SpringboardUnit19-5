from boggle import Boggle

from flask import Flask, request, render_template, redirect, flash, session, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start-game')
def start_game():
    current_game = boggle_game.make_board()
    session['current_game'] = current_game
    highscore = session.get("highscore", 0)

    return render_template("start_game.html", board = current_game, highscore = highscore)

@app.route('/check-guess')
def check_guess():
    guess = request.args["guess"]
    current_game = session["current_game"]
    res = boggle_game.check_valid_word(current_game, guess)

    return jsonify({'result': res})

@app.route('/add-score', methods=["POST"])
def add_score():
    score = request.json["score"]

    session['play_count'] = session.get("play_count", 0) + 1
    session['highscore'] = max(score, session.get("highscore", 0))

    return jsonify({'highscore': session.get("highscore")})

    # when there is a new highscore, only the DOM updates and the session variable does not until the user hits play again to refresh the page.