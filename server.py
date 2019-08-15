from flask import Flask, render_template, request, redirect, url_for, session
import data_manager
import hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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
    comments_for_question = data_manager.display_comments_for_question(question_id)
    # comments_for_answer = data_manager.display_comments_for_answer(answer_id)
    return render_template('display_question.html', question=question, answers=answers, comments_for_question=comments_for_question)


@app.route('/ask_question', methods=['GET', 'POST'])
def route_ask_question():
    new_question = {}
    if request.method == 'POST':
        new_question = {
            'id': data_manager.get_next_id('question'),
            'users_id': None,
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
            'users_id': None,
            'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'vote_number': '0',
            'question_id': question_id,
            'message': request.form.get('message'),
            'image': None
        }
        data_manager.insert_into_database('answer', answer)
        return redirect(url_for('route_questions', question_id=question_id))
    return render_template('post_answer.html', answer=answer, id=question_id)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def route_add_comment_to_question(question_id):
    comment = {}

    if request.method == 'POST':
        comment = {
            'id': data_manager.get_next_id('comment'),
            'users_id' : None,
            'question_id': question_id,
            'answer_id': None,
            'message': request.form.get('message'),
            'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'edited_count': 0
        }
        data_manager.insert_into_database('comment', comment)
        return redirect(url_for('route_questions', question_id=question_id))

    return render_template('add_comment_to_question.html', comment=comment, id=question_id)


@app.route('/question/<question_id>/<answer_id>/new-comment', methods=['GET', 'POST'])
def route_add_comment_to_answer(question_id, answer_id):
    comment = {}

    if request.method == 'POST':
        comment = {
            'id': data_manager.get_next_id('comment'),
            'users_id': None,
            'question_id': None,
            'answer_id': answer_id,
            'message': request.form.get('message'),
            'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'edited_count': 0
        }
        data_manager.insert_into_database('comment', comment)
        return redirect(url_for('route_questions', question_id=question_id))

    return render_template('add_comment_to_answer.html', comment=comment, question_id=question_id, answer_id=answer_id)


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def route_delete_question(question_id):
    data_manager.delete_from_database(question_id, question=True)
    return redirect('/')


@app.route('/question/<question_id>/<answer_id>/delete', methods=['GET', 'POST'])
def route_delete_answer(question_id, answer_id):
    data_manager.delete_from_database(answer_id)
    return redirect(url_for('route_questions', question_id=question_id))


@app.route('/question/<question_id>/vote-up', methods=['GET', 'POST'])
def route_vote_up(question_id):
    increment = 1
    print("up")
    if request.method == 'POST':
        answer_id = request.args.get('answer_id')
        data_manager.update_question_vote('answer', increment, id=answer_id)
    else:
        data_manager.update_question_vote('question', increment, id=question_id)
    return redirect(url_for('route_questions', question_id=question_id))


@app.route('/question/<question_id>/vote-down', methods=['GET', 'POST'])
def route_vote_down(question_id):
    increment = -1
    print("down")
    if request.method == 'POST':
        answer_id = request.args.get('answer_id')
        data_manager.update_question_vote('answer', increment, id=answer_id)
    else:
        data_manager.update_question_vote('question', increment, id=question_id)
    return redirect(url_for('route_questions', question_id=question_id))


@app.route('/search')
def search_questions_answers():
    search_phrase = request.args.get('search_phrase')
    results = data_manager.search_in_db(search_phrase.lower())
    return render_template('search_results.html', results=results, keyword=search_phrase)


@app.route('/registration', methods=['GET', 'POST'])
def route_registration():
    if request.method == "POST":
        registration_data = {
            'id': data_manager.get_next_id('users'),
            'username': request.form.get('username'),
            'password': hash.hash_password(request.form.get('password')),
            'email': request.form.get('email'),
            'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data_manager.insert_into_database('users', registration_data)
        return redirect('/list')
    else:
        return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def route_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        login_info = data_manager.get_user_login_info(username)
        if login_info and hash.verify_password(password, login_info['password']):
            session['username'] = username
        else:
            session['username'] = 'invalid'
        return redirect('/list')


@app.route('/logout')
def route_logout():
    session['username'] = None
    return redirect('/list')


@app.route('/users')
def route_users():
    users = data_manager.get_user_data()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True
    )
