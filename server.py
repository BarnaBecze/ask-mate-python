from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    return render_template('questions.html')


@app.route('/question/<question_id>')
def route_questions(question_id):
    return render_template('questions.html')


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True
    )