from classes import Ticket
from pathlib import Path
import csv

def test_create_ticket():
    data = {'duration': 20, 'price': 1.7, 'discount_type': 'normal'}
    ticket1 = Ticket(0, data)
    assert ticket1.id == 0
    assert ticket1.data == data


def test_save_to_file():
    data = {'duration': 20, 'price': 1.7, 'discount_type': 'normal'}
    ticket1 = Ticket(0, data)
    ticket1.save_to_file()
    path = Path('0.txt')
    assert path.is_file()
    with open('0.txt', 'r') as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            assert int(row['id']) == 0
            assert int(row['duration']) == 20
            assert float(row['price']) == 1.7
            assert row['discount_type'] == 'normal'
