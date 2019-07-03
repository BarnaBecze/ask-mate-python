import csv

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def read_csv_data(filename, filter=None):
    requested_data = []

    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if filter:
                if row['id'] == filter:
                    return row
            data = dict(row)
            requested_data.append(data)

    return requested_data


def write_csv_data(data, filename, header, append=False, remove=False):
    existing_data = read_csv_data(filename)

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()

        for row in existing_data:
            if not append and not remove:
                if row['id'] == data['id']:
                    row = data
            if not remove or row['id'] != data['id']:
                writer.writerow(row)

        if append:
            writer.writerow(data)
