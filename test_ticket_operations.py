
import pytest
from pathlib import Path
from datetime import date, timedelta
from ticket_operations import (
    choose_id,
    buy_short_term_ticket,
    buy_long_term_ticket,
    get_ticket_from_database,
    can_ticket_be_prolonged,
    buy_prepaid_ticket,
    get_prepaid_ticket_from_database,
    check_prepaid_balance,
    use_prepaid_ticket
)
from input_output_functions import (
    read_from_csv,
    write_to_csv
)
from classes import (
    Long_Term_Ticket,
    Prepaid_Ticket,
    InvalidPathError,
    InvalidTicketDataError,
    TicketTypeNotFoundError,
    InvalidDataError,
    Ticket_Not_in_DatabaseError
)


def test_choose_id():
    database_path = './test_ticket_database/long_term_tickets'
    with open(database_path + './last_id.txt', 'w') as file_handle:
        file_handle.write('-1')
    assert choose_id(database_path) == 0
    assert choose_id(database_path) == 1


def test_choose_id_invalid_path():
    database_path = './test_ticket_database/invalid_path'
    if Path(database_path).is_dir():
        Path(database_path).unlink()
    with pytest.raises(InvalidPathError):
        choose_id(database_path)

    database_path = './test_ticket_database'
    if Path(database_path + '/last_id.txt').is_file():
        Path(database_path + '/last_id.txt').unlink()
    with pytest.raises(InvalidPathError):
        choose_id(database_path)


def test_choose_id_invalid_data():
    database_path = './test_ticket_database/long_term_tickets'
    with open(database_path + './last_id.txt', 'w') as file_handle:
        file_handle.write('a')
    with pytest.raises(InvalidDataError):
        assert choose_id(database_path)


def test_buy_short_term_ticket_no_data_yet():
    ticket_to_buy = {'name': '20_min_reduced', 'price': '1.7'}

    folder_path = './test_ticket_database'
    file_path = folder_path + './short_term_tickets_data.txt'
    if Path(file_path).is_file():
        Path(file_path).unlink()

    buy_short_term_ticket(ticket_to_buy, folder_path)
    assert Path(file_path).is_file() == 1
    ticket_data = read_from_csv(folder_path + './short_term_tickets_data')
    for ticket_type in ticket_data:
        if ticket_type['ticket_type'] == ticket_to_buy['name']:
            assert ticket_type['number_sold'] == '1'
        else:
            assert ticket_type['number_sold'] == '0'


def test_buy_short_term_ticket_data_exists():
    ticket_types_file = './available_ticket_types/short_term_ticket_types'
    available_ticket_types = read_from_csv(ticket_types_file)
    ticket_to_buy = {'name': '20_min_reduced', 'price': '1.7'}

    folder_path = './test_ticket_database'
    file_path = folder_path + './short_term_tickets_data.txt'

    tickets_data_from_database = []
    for ticket_type in available_ticket_types:
        tickets_data_from_database.append({
                'ticket_type': ticket_type['name'],
                'number_sold': 0
        })
    write_to_csv(
        folder_path + './short_term_tickets_data',
        tickets_data_from_database,
        ['ticket_type', 'number_sold']
    )

    buy_short_term_ticket(ticket_to_buy, folder_path)
    assert Path(file_path).is_file() == 1
    ticket_data = read_from_csv(folder_path + './short_term_tickets_data')
    for ticket_type in ticket_data:
        if ticket_type['ticket_type'] == ticket_to_buy['name']:
            assert ticket_type['number_sold'] == '1'
        else:
            assert ticket_type['number_sold'] == '0'


def test_buy_short_term_ticket_invalid_path():
    ticket_to_buy = {'name': '20_min_reduced', 'price': '1.7'}
    folder_path = './test_ticket_database/invalid_path'
    if Path(folder_path).is_dir():
        Path(folder_path).unlink()
    with pytest.raises(InvalidPathError):
        buy_short_term_ticket(ticket_to_buy, folder_path)


def test_buy_short_term_ticket_invalid_ticket_data():
    ticket_types_file = './available_ticket_types/short_term_ticket_types'
    available_ticket_types = read_from_csv(ticket_types_file)

    folder_path = './test_ticket_database'
    file_path = folder_path + './short_term_tickets_data'

    tickets_data_from_database = []
    for ticket_type in available_ticket_types:
        tickets_data_from_database.append({
                'ticket_type': ticket_type['name'],
                'number_sold': 0
        })
    write_to_csv(
        file_path,
        tickets_data_from_database,
        ['ticket_type', 'number_sold']
    )

    ticket_to_buy = {'price': '1.7'}
    with pytest.raises(InvalidTicketDataError):
        buy_short_term_ticket(ticket_to_buy, folder_path)
        tickets_data_after_invalid = read_from_csv(file_path)
        assert tickets_data_after_invalid == tickets_data_from_database


def test_buy_short_term_ticket_ticket_type_not_found():
    ticket_types_file = './available_ticket_types/short_term_ticket_types'
    available_ticket_types = read_from_csv(ticket_types_file)

    folder_path = './test_ticket_database'
    file_path = folder_path + './short_term_tickets_data'

    tickets_data_from_database = []
    for ticket_type in available_ticket_types:
        tickets_data_from_database.append({
                'ticket_type': ticket_type['name'],
                'number_sold': 0
        })
    write_to_csv(
        file_path,
        tickets_data_from_database,
        ['ticket_type', 'number_sold']
    )

    ticket_to_buy = {'name': 'not_a_type', 'price': '1.7'}
    with pytest.raises(TicketTypeNotFoundError):
        buy_short_term_ticket(ticket_to_buy, folder_path)
        tickets_data_after_invalid = read_from_csv(file_path)
        assert tickets_data_after_invalid == tickets_data_from_database


def test_buy_long_term_ticket():
    ticket_type = {
        'name': '30_day_reduced',
        'duration': '30',
        'price': '55'
    }
    folder_path = './test_ticket_database/long_term_tickets'
    with open(folder_path + './last_id.txt', 'w') as file_handle:
        file_handle.write('-1')
    if Path(folder_path + './0.txt').is_file():
        Path(folder_path + './0.txt').unlink()
    assert buy_long_term_ticket(ticket_type, folder_path) == 0
    assert Path(folder_path + './0.txt').is_file()
    ticket_data = read_from_csv(folder_path + './0')
    today = date.today().isoformat()
    expected_ticket_data = {
        'id': '0',
        'date_of_purchase': today,
        'duration': '30'
    }
    assert ticket_data[0] == expected_ticket_data


def test_buy_long_term_ticket_invalid_ticket_data():
    folder_path = './test_ticket_database/long_term_tickets'
    with pytest.raises(InvalidTicketDataError):
        buy_long_term_ticket(
            {'name': '30_day_reduced', 'price': '55'},
            folder_path
        )
    with pytest.raises(InvalidTicketDataError):
        buy_long_term_ticket(
            {'name': '30_day_reduced', 'duration': 'a', 'price': '55'},
            folder_path
        )


def test_get_ticket_from_database_exists():
    folder_path = './test_ticket_database/long_term_tickets'
    if Path(folder_path + './0.txt').is_file():
        Path(folder_path + './0.txt').unlink()
    Long_Term_Ticket(0, date.today().isoformat(), 30, folder_path)
    ticket = get_ticket_from_database(0, folder_path)
    assert ticket.id == 0
    assert ticket.date_of_purchase == date.today().isoformat()
    assert ticket.duration == 30


def test_get_ticket_from_database_does_not_exists():
    folder_path = './test_ticket_database/long_term_tickets'
    if Path(folder_path + './0.txt').is_file():
        Path(folder_path + './0.txt').unlink()
    with pytest.raises(Ticket_Not_in_DatabaseError):
        get_ticket_from_database(0, folder_path)


def test_can_ticket_be_prolonged_yes():
    folder_path = './test_ticket_database/long_term_tickets'
    if Path(folder_path + './0.txt').is_file():
        Path(folder_path + './0.txt').unlink()
    today = date.today()
    date_of_purchase = today - timedelta(31)
    Long_Term_Ticket(0, date_of_purchase.isoformat(), 30, folder_path)
    assert can_ticket_be_prolonged(0, folder_path) == [1, 7]

    Path(folder_path + './0.txt').unlink()
    date_of_purchase = today - timedelta(23)
    Long_Term_Ticket(0, date_of_purchase.isoformat(), 30, folder_path)
    assert can_ticket_be_prolonged(0, folder_path) == [1, 7]


def test_can_ticket_be_prolonged_no():
    folder_path = './test_ticket_database/long_term_tickets'
    if Path(folder_path + './0.txt').is_file():
        Path(folder_path + './0.txt').unlink()
    today = date.today()
    date_of_purchase = today - timedelta(1)
    Long_Term_Ticket(0, date_of_purchase.isoformat(), 30, folder_path)
    assert can_ticket_be_prolonged(0, folder_path) == [0, 7]


def test_buy_prepaid_ticket():
    ticket_type = {'value': '200'}
    folder_path = './test_ticket_database/prepaid_tickets'
    with open(folder_path + './last_id.txt', 'w') as file_handle:
        file_handle.write('-1')
    if Path(folder_path + './0.txt').is_file():
        Path(folder_path + './0.txt').unlink()
    assert buy_prepaid_ticket(ticket_type, folder_path) == 0
    assert Path(folder_path + './0.txt').is_file()
    ticket_data = read_from_csv(folder_path + './0')
    expected_ticket_data = {'id': '0', 'balance': '200.0'}
    assert ticket_data[0] == expected_ticket_data


def test_get_prepaid_ticket_from_database_exists():
    folder_path = './test_ticket_database/prepaid_tickets'
    if Path(folder_path + './0.txt').is_file():
        Path(folder_path + './0.txt').unlink()
    Prepaid_Ticket(0, 50.0, folder_path)
    ticket = get_prepaid_ticket_from_database(0, folder_path)
    assert ticket.id == 0
    assert ticket.balance == 50.0


def test_get_prepaid_ticket_from_database_does_not_exists():
    folder_path = './test_ticket_database/prepaid_tickets'
    if Path(folder_path + './0.txt').is_file():
        Path(folder_path + './0.txt').unlink()
    with pytest.raises(Ticket_Not_in_DatabaseError):
        get_prepaid_ticket_from_database(0, folder_path)


def test_use_prepaid_ticket_balance_enough():
    folder_path = './test_ticket_database/prepaid_tickets'
    bought_ticket = {'name': '90_min_standard', 'price': '7'}

    if Path(folder_path + './0.txt').is_file():
        Path(folder_path + './0.txt').unlink()
    Prepaid_Ticket(0, 8.0, folder_path)
    assert use_prepaid_ticket(0, bought_ticket, './test_ticket_database') == 1
    assert check_prepaid_balance(0, folder_path) == 1.0

    Path(folder_path + './0.txt').unlink()
    Prepaid_Ticket(0, 7.0, folder_path)
    assert use_prepaid_ticket(0, bought_ticket, './test_ticket_database') == 1
    assert check_prepaid_balance(0, folder_path) == 0.


def test_use_prepaid_ticket_balance_not_enough():
    folder_path = './test_ticket_database/prepaid_tickets'
    bought_ticket = {'name': '90_min_standard', 'price': '7'}
    if Path(folder_path + './0.txt').is_file():
        Path(folder_path + './0.txt').unlink()
    Prepaid_Ticket(0, 6.0, folder_path)
    assert use_prepaid_ticket(0, bought_ticket, './test_ticket_database') == 0
    assert check_prepaid_balance(0, folder_path) == 6.0
