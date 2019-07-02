from connection import read_csv_data, write_csv_data


def list_questions():
    questions = read_csv_data('sample_data/question.csv')
    return sorted(questions, key=lambda q: q['submission_time'], reverse=True)


def display_question(question_title):
    questions = read_csv_data('sample_data/question.csv')
    for question in questions:
        if question['title'] == question_title:
            answer = dict(read_csv_data('sample_data/answer.csv', question['id']))
            return question, answer

def ask_question():
    pass