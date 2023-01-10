from classes import (
    Ticket,
    Long_Term_Time_Ticket,
    Long_Term_Prepaid_Ticket
    )
from pathlib import Path
from datetime import date, timedelta
import csv


def test_create_Ticket():
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


def test_create_Long_Term_Time_Ticket():
    data = {'duration': 30, 'date_of_purchase': '2022-12-20', 'price': 49, 'discount_type': 'discount'}
    ticket1 = Long_Term_Time_Ticket(1, data)
    assert ticket1.id == 1
    assert ticket1.data == data


def test_check_status_Long_Term_Time_Ticket():
    today = date.today()
    date_of_purchase = today - timedelta(days=1)
    date_of_purchase = date_of_purchase.isoformat()

    data = {'duration': 30, 'date_of_purchase': date_of_purchase, 'price': 49, 'discount_type': 'discount'}
    ticket1 = Long_Term_Time_Ticket(1, data)

    days_left = ticket1.check_status()
    assert days_left == timedelta(days=29)


def test_check_status_Long_Term_Time_Ticket_expired():
    today = date.today()
    date_of_purchase = today - timedelta(days=31)
    date_of_purchase = date_of_purchase.isoformat()

    data = {'duration': 30, 'date_of_purchase': date_of_purchase, 'price': 49, 'discount_type': 'discount'}
    ticket1 = Long_Term_Time_Ticket(1, data)

    days_left = ticket1.check_status()
    assert days_left == timedelta(days=0)
