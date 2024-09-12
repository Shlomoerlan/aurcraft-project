import csv
from toolz import pipe, pluck


def save_data(self, data):
    with open(self.file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        pipe(
            data,
            lambda rows: writer.writerow(rows[0].keys()),
            lambda _: writer.writerows(pluck('values', data))
        )
