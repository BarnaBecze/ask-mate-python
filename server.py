from flask import Flask, render_template
from data_manager import  list_questions, display_question, display_answers


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    questions = list_questions()
    return render_template('index.html', questions=questions)


@app.route('/question/<question_id>')
def route_questions(question_id):
    question = display_question(question_id)
    answers = display_answers(question_id)
    return render_template('questions.html', question=question, answers=answers)


@app.route('/question/<question_id>/new-answer')
def route_post_answer(question_id):
    pass


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True
    )