from connection import connection_handler
from psycopg2 import sql

@connection_handler
def list_questions(cursor, sort=None, direction=None, latest=None):
    if sort:
        cursor.execute(f'''
                        SELECT * FROM question
                        ORDER BY {sort} {direction};''')
    else:
        query = ('''
                 SELECT * FROM question
                 ORDER BY submission_time DESC
                 ''')
        if latest:
            query += 'LIMIT 5;'
        cursor.execute(query)
    questions = cursor.fetchall()
    return questions


@connection_handler
def display_question(cursor, question_id):
    cursor.execute('''
                    SELECT * FROM question
                    WHERE id='%s';
                    ''' % int(question_id))
    question = cursor.fetchall()

    return question[0]


@connection_handler
def display_answers(cursor, question_id=None):
    if question_id:
        cursor.execute('''
                        SELECT * FROM answer
                        WHERE question_id='%s';
                        ''' % question_id)
        answers = cursor.fetchall()
        return sorted(answers, key=lambda a: a['vote_number'])
    else:
        cursor.execute('SELECT * FROM answer')
        answers = cursor.fetchall()
        return answers

@connection_handler
def get_next_id(cursor, item_type):
    cursor.execute(f'SELECT MAX(id) AS max_id FROM {item_type};')
    max_id = cursor.fetchone()
    if max_id == 0:
        return 1
    return max_id['max_id'] + 1

@connection_handler
def update_question_vote(cursor, table, increment, id=None):
    query = sql.SQL(f'UPDATE {table} '
                    f'SET vote_number = vote_number + {increment} WHERE id = {id} AND vote_number BETWEEN -10 AND 200;')
    cursor.execute(query)


@connection_handler
def insert_into_database(cursor, table, data):
    query = sql.SQL('INSERT INTO {} '
                    'VALUES ({});').format(sql.Identifier(table), sql.SQL(', ').join(map(sql.Placeholder, data)))
    cursor.execute(query, data)


@connection_handler
def delete_from_database(cursor, id, question=False):

    if question:
        query_tag = '''DELETE FROM tag WHERE id = (SELECT tag_id FROM question_tag WHERE question_id = id)'''
        cursor.execute(query_tag)
        query_question_tag = f'DELETE FROM question_tag WHERE question_id={id}'
        cursor.execute(query_question_tag)
        query_comment_question = f'DELETE FROM comment WHERE question_id={id} OR answer_id IN (SELECT id FROM answer WHERE question_id={id})'
        cursor.execute(query_comment_question)
        query_answers = f'DELETE FROM answer WHERE question_id={id}'
        cursor.execute(query_answers)
        query_question = f'DELETE FROM question WHERE id={id}'
        cursor.execute(query_question)

    query_comment = f'DELETE FROM comment WHERE answer_id={id}'
    cursor.execute(query_comment)
    query_answer = f'DELETE FROM answer WHERE id={id}'
    cursor.execute(query_answer)


@connection_handler
def search_in_db(cursor, search_phrase):
    cursor.execute(f"""
                    SELECT * FROM answer
                    WHERE message LIKE '%{search_phrase}%';""")
    answers = cursor.fetchall()
    cursor.execute(f"""
                    SELECT * FROM question
                    WHERE message LIKE '%{search_phrase}%' OR title LIKE '%{search_phrase}%';""")
    questions = cursor.fetchall()
    return answers, questions