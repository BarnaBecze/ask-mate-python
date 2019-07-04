from connection import read_csv_data, write_csv_data


def list_questions():
    questions = read_csv_data('sample_data/question.csv')
    return sorted(questions, key=lambda q: q['submission_time'], reverse=True)


def display_question(question_id):
    questions = read_csv_data('sample_data/question.csv')
    for question in questions:
        if question['id'] == question_id:
            return question


def display_answers(question_id):
    answers = []
    every_answer = read_csv_data('sample_data/answer.csv')
    for answer in every_answer:
        if answer['question_id'] == question_id:
            answers.append(answer)
    return answers


def ask_question():
    pass


