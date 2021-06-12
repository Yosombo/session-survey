from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz
app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def show_home():
    return render_template('home.html', surveys=[satisfaction_survey])


# @app.route("/begin", methods=["POST"])
@app.route("/begin")
def start_survey():

    session['responses'] = []

    return redirect("/questions/0")


@app.route('/questions/<page>')
def show_questions(page):
    ind = int(page)
    responses = session.get('responses')
    if len(responses) == ind:
        return render_template('questions.html', title=satisfaction_survey.title, question=satisfaction_survey.questions[ind].question, choices=satisfaction_survey.questions[ind].choices)
    flash('You are trying to access an invalid question.')
    return redirect(f'/questions/{len(responses)}')


@app.route('/answer', methods=["POST", "GET"])
def answers():
    req = request.form.get('answer')
    responses = session['responses']
    responses.append(req)
    session['responses'] = responses
    if len(responses) == len(satisfaction_survey.questions):
        return render_template('thanks.html')
    return redirect(f'/questions/{len(responses)}')
