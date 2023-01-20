
import pytest
from datetime import date, timedelta
from pathlib import Path
from input_output_functions import (
    read_from_csv,
    write_to_csv
)
from classes import Long_Term_Ticket, Prepaid_Ticket


def remove_previous_file(folder_path: str, path: str):
    if Path(path + '.txt').is_file():
        Path(path + '.txt').unlink()
    assert Path(path + '.txt').is_file() == 0


def test_create_Long_Term_Ticket_new():
    folder_path = './test_ticket_database/long_term_tickets'
    path = folder_path + '/0'
    remove_previous_file(folder_path, path)

    ticket = Long_Term_Ticket(0, '2023-01-20', 30, folder_path)
    assert ticket.id == 0
    assert ticket.date_of_purchase == '2023-01-20'
    assert ticket.duration == 30
    assert ticket.path == folder_path + '/0'
    assert Path(path + '.txt').is_file()
    file = read_from_csv(path)
    assert len(file) == 1
    ticket_data = file[0]
    assert len(ticket_data) == 3
    assert ticket_data['id'] == '0'
    assert ticket_data['date_of_purchase'] == '2023-01-20'
    assert ticket_data['duration'] == '30'


def test_create_Long_Term_Ticket_data_already_exists():
    folder_path = './test_ticket_database/long_term_tickets'
    path = folder_path + '/0'
    ticket_data = [{
            'id': 0,
            'date_of_purchase': '2023-01-20',
            'duration': 30
        }]
    write_to_csv(path, ticket_data, ['id', 'date_of_purchase', 'duration'])
    assert Path(path + '.txt').is_file() == 1

    ticket = Long_Term_Ticket(0, '2023-01-20', 30, folder_path)
    assert ticket.id == 0
    assert ticket.date_of_purchase == '2023-01-20'
    assert ticket.duration == 30
    assert ticket.path == folder_path + '/0'
    assert Path(path + '.txt').is_file()
    file = read_from_csv(path)
    assert len(file) == 1
    ticket_data = file[0]
    assert len(ticket_data) == 3
    assert ticket_data['id'] == '0'
    assert ticket_data['date_of_purchase'] == '2023-01-20'
    assert ticket_data['duration'] == '30'


def test_create_Long_Term_Ticket_incorrect_data():
    pass


def test_Long_Term_Ticket_save_to_file_change_data():
    folder_path = './test_ticket_database/long_term_tickets'
    path = folder_path + '/0'
    remove_previous_file(folder_path, path)
    ticket = Long_Term_Ticket(0, '2023-01-20', 30, folder_path)
    ticket.duration = 35
    ticket.save_to_file()

    file = read_from_csv(path)
    assert len(file) == 1
    ticket_data = file[0]
    assert len(ticket_data) == 3
    assert ticket_data['id'] == '0'
    assert ticket_data['date_of_purchase'] == '2023-01-20'
    assert ticket_data['duration'] == '35'


def test_Long_Term_Ticket_check_status_active():
    folder_path = './test_ticket_database/long_term_tickets'
    path = folder_path + '/0'

    today = date.today()
    date_of_purchase = today - timedelta(days=1)
    date_of_expiration = date_of_purchase + timedelta(days=30)
    date_of_purchase = date_of_purchase.isoformat()
    date_of_expiration = date_of_expiration.isoformat()

    ticket = Long_Term_Ticket(0, date_of_purchase, 30, folder_path)
    ticket.save_to_file()
    status_info = ticket.check_status()
    assert status_info['days_left'] == 29
    assert status_info['expires'] == date_of_expiration


def test_Long_Term_Ticket_check_status_not_active():
    folder_path = './test_ticket_database/long_term_tickets'
    path = folder_path + '/0'

    today = date.today()
    date_of_purchase = today - timedelta(days=31)
    date_of_expiration = date_of_purchase + timedelta(days=30)
    date_of_purchase = date_of_purchase.isoformat()
    date_of_expiration = date_of_expiration.isoformat()

    ticket = Long_Term_Ticket(0, date_of_purchase, 30, folder_path)
    ticket.save_to_file()
    status_info = ticket.check_status()
    assert status_info['days_left'] == 0
    assert status_info['expires'] == date_of_expiration


def test_Long_Term_Ticket_prolong_extend():
    folder_path = './test_ticket_database/long_term_tickets'
    path = folder_path + '/0'
    today = date.today()
    date_of_purchase = (today - timedelta(days=20)).isoformat()
    ticket = Long_Term_Ticket(0, date_of_purchase, 30, folder_path)
    ticket.save_to_file()

    ticket.prolong_ticket(10)
    assert ticket.date_of_purchase == today.isoformat()
    assert ticket.duration == 20


def test_Long_Term_Ticket_prolong_reload_expired():
    folder_path = './test_ticket_database/long_term_tickets'
    path = folder_path + '/0'
    today = date.today()
    date_of_purchase = (today - timedelta(days=31)).isoformat()
    ticket = Long_Term_Ticket(0, date_of_purchase, 30, folder_path)
    ticket.save_to_file()

    ticket.prolong_ticket(10)
    assert ticket.date_of_purchase == today.isoformat()
    assert ticket.duration == 10


def test_Long_Term_Ticket_prolong_negative_duration():
    folder_path = './test_ticket_database/long_term_tickets'
    path = folder_path + '/0'
    ticket = Long_Term_Ticket(0, '2023-01-20', 30, folder_path)
    ticket.save_to_file()
    with pytest.raises(Exception):
        ticket.prolong_ticket(-1)
