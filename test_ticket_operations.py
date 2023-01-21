
import pytest
from pathlib import Path
from ticket_operations import (
    choose_id,
    buy_short_term_ticket,
    buy_long_term_ticket,
    get_ticket_from_database,
    InvalidPathError,
    InvalidTicketDataError,
    TicketTypeNotFoundError,
    InvalidDataError
)
from input_output_functions import (
    read_from_csv,
    write_to_csv
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


# def test_use_prepaid_ticket():
#     file_short_term_types = './available_ticket_types/short_term_ticket_types'
#     file_prepaid_types = './available_ticket_types/prepaid_ticket_types'
#     prepaid_type = read_from_csv(file_prepaid_types)[0]
#     bought_ticket = read_from_csv(file_short_term_types)[0]
#     id = choose_id('./ticket_database/prepaid_tickets') + 1

#     buy_prepaid_ticket(prepaid_type)
#     use_prepaid_ticket(id, bought_ticket)
#     recharge_prepaid_ticket(id, prepaid_type)
#     use_prepaid_ticket(id, bought_ticket)
#     assert check_prepaid_balance(id) == 36.6
