from flask import Flask, render_template, request, redirect, url_for
from data_manager import list_questions, display_question, display_answers, get_next_id, convert_timestamp_to_datetime, get_current_time
import connection

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
    return render_template('questions.html', question=convert_timestamp_to_datetime(question), answers=answers)


@app.route('/ask_question', methods=['GET', 'POST'])
def route_ask_question():
    new_question = {}
    if request.method == 'POST':
        new_question = {
            'id': get_next_id('sample_data/question.csv'),
            'submission_time': get_current_time(),
            'view_number': 100,
            'vote_number': 100,
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': 100

        }
        connection.write_csv_data(new_question, 'sample_data/question.csv', connection.QUESTION_HEADER)
        return redirect(url_for('route_questions', question_id=new_question['id']))
    return render_template('ask_question.html', new_question=new_question)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_post_answer(question_id):
    answer = {}
    if request.method == 'POST':
        answer = {
            'id': 100,
            'submission_time': 100,
            'vote_number': 0,
            'question_id': question_id,
            'message': request.form.get('message'),
            'image': 100
        }
        connection.write_csv_data(answer, 'sample_data/answer.csv', connection.ANSWER_HEADER)
        return redirect(url_for('route_questions', question_id=question_id))
    return render_template('answers.html', answer=answer, id=question_id)


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True
    )
