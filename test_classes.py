
import pytest
from datetime import date, timedelta
from pathlib import Path
from input_output_functions import (
    read_from_csv,
    write_to_csv
)
from classes import (
    Long_Term_Ticket,
    Prepaid_Ticket,
    InvalidTicketPropertyError,
    ExtendingCannotBeNegativeError
)


def remove_previous_file(path: str):
    if Path(path + '.txt').is_file():
        Path(path + '.txt').unlink()


def test_create_Long_Term_Ticket_new():
    folder_path = './test_ticket_database/long_term_tickets'
    path = folder_path + '/0'
    remove_previous_file(path)

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


def test_create_Long_Term_Ticket_incorrect_data():
    invalid_date = (date.today() + timedelta(days=1)).isoformat()
    folder_path = './test_ticket_database/long_term_tickets'
    with pytest.raises(InvalidTicketPropertyError):
        Long_Term_Ticket(-1, '2023-01-20', 30, folder_path)
    with pytest.raises(InvalidTicketPropertyError):
        Long_Term_Ticket(0, invalid_date, 30, folder_path)
    with pytest.raises(InvalidTicketPropertyError):
        Long_Term_Ticket(0, '2023-01-20', -5, folder_path)


def test_Long_Term_Ticket_save_to_file_change_data():
    folder_path = './test_ticket_database/long_term_tickets'
    path = folder_path + '/0'
    remove_previous_file(path)
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
    today = date.today()
    date_of_purchase = (today - timedelta(days=20)).isoformat()
    ticket = Long_Term_Ticket(0, date_of_purchase, 30, folder_path)
    ticket.save_to_file()

    ticket.prolong_ticket(10)
    assert ticket.date_of_purchase == today.isoformat()
    assert ticket.duration == 20


def test_Long_Term_Ticket_prolong_reload_expired():
    folder_path = './test_ticket_database/long_term_tickets'
    today = date.today()
    date_of_purchase = (today - timedelta(days=31)).isoformat()
    ticket = Long_Term_Ticket(0, date_of_purchase, 30, folder_path)
    ticket.save_to_file()

    ticket.prolong_ticket(10)
    assert ticket.date_of_purchase == today.isoformat()
    assert ticket.duration == 10


def test_Long_Term_Ticket_prolong_negative_duration():
    folder_path = './test_ticket_database/long_term_tickets'
    ticket = Long_Term_Ticket(0, '2023-01-20', 30, folder_path)
    ticket.save_to_file()
    with pytest.raises(ExtendingCannotBeNegativeError):
        ticket.prolong_ticket(-1)


def test_create_Prepaid_Ticket_new():
    folder_path = './test_ticket_database/prepaid_tickets'
    path = folder_path + '/0'
    remove_previous_file(path)

    ticket = Prepaid_Ticket(0, 200.0, folder_path)
    assert ticket.id == 0
    assert ticket.balance == 200.0
    assert ticket.path == folder_path + '/0'
    assert Path(path + '.txt').is_file()
    file = read_from_csv(path)
    assert len(file) == 1
    ticket_data = file[0]
    assert len(ticket_data) == 2
    assert ticket_data['id'] == '0'
    assert ticket_data['balance'] == '200.0'


def test_create_Prepaid_Ticket_data_already_exists():
    folder_path = './test_ticket_database/prepaid_tickets'
    path = folder_path + '/0'
    ticket_data = [{
            'id': 0,
            'balance': 200.0
        }]
    write_to_csv(path, ticket_data, ['id', 'balance'])
    assert Path(path + '.txt').is_file() == 1

    ticket = Prepaid_Ticket(0, 200.0, folder_path)
    assert ticket.id == 0
    assert ticket.balance == 200.0
    assert ticket.path == folder_path + '/0'


def test_create_Prepaid_Ticket_incorrect_data():
    folder_path = './test_ticket_database/prepaid_tickets'
    path = folder_path + '/0'

    remove_previous_file(path)
    with pytest.raises(InvalidTicketPropertyError):
        Prepaid_Ticket(-1, 200.0, folder_path)
    remove_previous_file(path)
    with pytest.raises(InvalidTicketPropertyError):
        Prepaid_Ticket(0, -5.0, folder_path)


def test_Prepaid_Ticket_save_to_file_change_data():
    folder_path = './test_ticket_database/prepaid_tickets'
    path = folder_path + '/0'
    remove_previous_file(path)
    ticket = Prepaid_Ticket(0, 200.0, folder_path)
    ticket.balance = 170.0
    ticket.save_to_file()

    file = read_from_csv(path)
    assert len(file) == 1
    ticket_data = file[0]
    assert len(ticket_data) == 2
    assert ticket_data['id'] == '0'
    assert ticket_data['balance'] == '170.0'


def test_Prepaid_Ticket_check_balance_positive():
    folder_path = './test_ticket_database/prepaid_tickets'
    ticket = Prepaid_Ticket(0, 200.0, folder_path)
    ticket.save_to_file()
    assert ticket.check_balance() == 200.0


def test_Prepaid_Ticket_check_balance_zero():
    folder_path = './test_ticket_database/prepaid_tickets'
    ticket = Prepaid_Ticket(0, 0.0, folder_path)
    ticket.save_to_file()
    assert ticket.check_balance() == 0.0


def test_Prepaid_Ticket_recharge_ticket_from_not_zero():
    folder_path = './test_ticket_database/prepaid_tickets'
    ticket = Prepaid_Ticket(0, 50.0, folder_path)
    ticket.save_to_file()
    ticket.recharge_ticket(50.0)
    assert ticket.check_balance() == 100.0


def test_Prepaid_Ticket_recharge_ticket_from_zero():
    folder_path = './test_ticket_database/prepaid_tickets'
    ticket = Prepaid_Ticket(0, 0.0, folder_path)
    ticket.save_to_file()
    ticket.recharge_ticket(50.0)
    assert ticket.check_balance() == 50.0


def test_Prepaid_Ticket_recharge_ticket_value_negative():
    folder_path = './test_ticket_database/prepaid_tickets'
    ticket = Prepaid_Ticket(0, 50.0, folder_path)
    ticket.save_to_file()
    with pytest.raises(ExtendingCannotBeNegativeError):
        ticket.recharge_ticket(-50.0)
    assert ticket.check_balance() == 50.0


def test_Prepaid_Ticket_use_prepaid_can_afford():
    folder_path = './test_ticket_database/prepaid_tickets'
    ticket = Prepaid_Ticket(0, 50.0, folder_path)
    ticket.save_to_file()
    assert ticket.use_prepaid(40.0) == 1
    assert ticket.check_balance() == 10.0


def test_Prepaid_Ticket_use_prepaid_cannot_afford():
    folder_path = './test_ticket_database/prepaid_tickets'
    ticket = Prepaid_Ticket(0, 30.0, folder_path)
    ticket.save_to_file()
    assert ticket.use_prepaid(40.0) == 0
    assert ticket.check_balance() == 30.0

    ticket = Prepaid_Ticket(0, 0.0, folder_path)
    ticket.save_to_file()
    assert ticket.use_prepaid(40.0) == 0
    assert ticket.check_balance() == 0.0


def test_Prepaid_Ticket_use_prepaid_price_negative():
    folder_path = './test_ticket_database/prepaid_tickets'
    ticket = Prepaid_Ticket(0, 30.0, folder_path)
    ticket.save_to_file()
    with pytest.raises(ExtendingCannotBeNegativeError):
        ticket.use_prepaid(-10.0)
