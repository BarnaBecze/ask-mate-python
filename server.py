from flask import Flask, render_template, request, redirect, url_for
import data_manager
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def list_latest_questions():
    latest_questions = data_manager.list_questions(latest=True)
    return render_template('index.html', latest=True, questions=latest_questions)


@app.route('/list', methods=['GET', 'POST'])
def index():
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    questions = data_manager.list_questions(sort, direction)
    return render_template('index.html', questions=questions)


@app.route('/question/<question_id>')
def route_questions(question_id):
    question = data_manager.display_question(question_id)
    answers = data_manager.display_answers(question_id)
    return render_template('questions.html', question=question, answers=answers)


@app.route('/ask_question', methods=['GET', 'POST'])
def route_ask_question():
    new_question = {}
    if request.method == 'POST':
        new_question = {
            'id': data_manager.get_next_id('question'),
            'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'view_number': '0',
            'vote_number': '0',
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': None

        }
        data_manager.insert_into_database('question', new_question)
        return redirect(url_for('route_questions', question_id=new_question['id']))
    return render_template('ask_question.html', new_question=new_question)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_post_answer(question_id):
    answer = {}
    if request.method == 'POST':
        answer = {
            'id': data_manager.get_next_id('answer'),
            'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'vote_number': '0',
            'question_id': question_id,
            'message': request.form.get('message'),
            'image': None
        }
        data_manager.insert_into_database('answer', answer)
        return redirect(url_for('route_questions', question_id=question_id))
    return render_template('answers.html', answer=answer, id=question_id)


@app.route('/question/<question_id>/delete', methods=['GET', 'DELETE'])
def route_delete_question(question_id):
    data_manager.delete_from_database(question_id, question=True)
    return redirect('/')


@app.route('/question/<question_id>/<answer_id>/delete', methods=['GET', 'DELETE'])
def route_delete_answer(question_id, answer_id):
    data_manager.delete_from_database(answer_id)
    return redirect(url_for('route_questions', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def route_add_comment(question_id):
    comment = {}
    if request.method == 'POST':
        comment = {
            'id': data_manager.get_next_id('comment'),
            'question_id': question_id,
            'answer_id': None,
            'message': request.form.get('message'),
            'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'edited_count': 0
        }
        data_manager.insert_into_database('comment', comment)
        return redirect(url_for('route_questions', question_id=question_id))
    return render_template('comment.html', comment=comment, id=question_id)


@app.route('/question/<question_id>/vote-up', methods=['GET', 'POST'])
def route_vote_up(question_id, answer_id=None):
    increment = 1
    if request.method == 'POST':
        data_manager.update_question_vote('answer', question_id,  increment, answer_id)
    else:
        data_manager.update_question_vote('question', question_id, increment)


@app.route('/question/<question_id>/vote-down', methods=['GET', 'POST'])
def route_vote_down(question_id, answer_id=None):
    increment = -1
    if request.method == 'POST':
        data_manager.update_question_vote('answer', question_id,  increment, answer_id)
    else:
        data_manager.update_question_vote('question', question_id, increment)
    return redirect(url_for('route_questions', question_id=question_id))


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True
    )
