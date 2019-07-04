from connection import read_csv_data, write_csv_data
from datetime import datetime
import time


def convert_timestamp_to_datetime(data):
    data['submission_time'] = datetime.fromtimestamp(int(data['submission_time']))
    return data


def list_questions():
    questions = read_csv_data('sample_data/question.csv')
    ordered_questions = sorted(questions, key=lambda q: q['submission_time'], reverse=True)

    return ordered_questions


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
    return sorted(answers, key=lambda a: a['vote_number'])


def get_next_id(filename):
    existing_data = read_csv_data(filename)

    if len(existing_data) == 0:
        return '1'

    return str(int(existing_data[-1]['id']) + 1)


def get_current_time():
    current_time = int(time.time())
    return current_time


