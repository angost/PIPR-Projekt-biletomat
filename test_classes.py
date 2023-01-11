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


def test_recharge_Long_Term_Time_Ticket_extend():
    today = date.today()
    date_of_purchase = today - timedelta(days=29)
    date_of_purchase = date_of_purchase.isoformat()
    data = {'duration': 30, 'date_of_purchase': date_of_purchase, 'price': 49, 'discount_type': 'discount'}
    ticket1 = Long_Term_Time_Ticket(1, data)

    assert ticket1.data['duration'] == 30
    assert ticket1.data['date_of_purchase'] == date_of_purchase
    assert ticket1.check_status() == timedelta(days=1)
    ticket1.recharge_ticket(30)
    assert ticket1.data['duration'] == 31
    assert ticket1.data['date_of_purchase'] == today.isoformat()
    assert ticket1.check_status() == timedelta(days=31)


def test_recharge_Long_Term_Time_Ticket_reload_expired():
    today = date.today()
    date_of_purchase = today - timedelta(days=31)
    date_of_purchase = date_of_purchase.isoformat()
    data = {'duration': 30, 'date_of_purchase': date_of_purchase, 'price': 49, 'discount_type': 'discount'}
    ticket1 = Long_Term_Time_Ticket(1, data)

    assert ticket1.data['duration'] == 30
    assert ticket1.data['date_of_purchase'] == date_of_purchase
    assert ticket1.check_status() == timedelta(days=0)
    ticket1.recharge_ticket(30)
    assert ticket1.data['duration'] == 30
    assert ticket1.data['date_of_purchase'] == today.isoformat()
    assert ticket1.check_status() == timedelta(days=30)


def test_create_Long_Term_Prepaid_Ticket():
    data = {'balance': 20.0, 'active_ticket': None}
    ticket2 = Long_Term_Prepaid_Ticket(2, data)
    assert ticket2.id == 2
    assert ticket2.data == data


def test_check_balance_Long_Term_Prepaid_Ticket():
    data = {'balance': 20.0, 'active_ticket': None}
    ticket2 = Long_Term_Prepaid_Ticket(2, data)
    assert ticket2.check_balance() == 20.0


def test_check_balance_Long_Term_Prepaid_Ticket_empty():
    data = {'balance': 0, 'active_ticket': None}
    ticket2 = Long_Term_Prepaid_Ticket(2, data)
    assert ticket2.check_balance() == 0.0


def test_recharge_Long_Term_Prepaid_Ticket():
    data = {'balance': 20.0, 'active_ticket': None}
    ticket2 = Long_Term_Prepaid_Ticket(2, data)
    assert ticket2.check_balance() == 20.0
    with open('2.txt', 'r') as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            assert float(row['balance']) == 20.0

    ticket2.recharge_ticket(5)

    assert ticket2.check_balance() == 25.0
    with open('2.txt', 'r') as file_handle2:
        reader2 = csv.DictReader(file_handle2)
        for row in reader2:
            assert float(row['balance']) == 25.0


def test_use_prepaid_Long_Term_Prepaid_Ticket():
    data = {'balance': 20.0, 'active_ticket': None}
    ticket1 = Long_Term_Prepaid_Ticket(1, data)
    assert ticket1.check_balance() == 20.0

    ticket_to_asign_data = {'duration': 20, 'price': 1.7, 'discount_type': 'normal'}
    ticket_to_asign = Ticket(0, ticket_to_asign_data)

    ticket1.use_prepaid(ticket_to_asign, ticket_to_asign.data['price'])
    assert ticket1.check_balance() == 20.0 - 1.7
    assert ticket1.data['current_ticket'] == ticket_to_asign
