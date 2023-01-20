
import pytest
from pathlib import Path
from ticket_operations import (
    choose_id,
    buy_long_term_ticket,
    get_ticket_from_database
)
from input_output_functions import (
    read_from_csv
)


def test_choose_id():
    database_path = './test_ticket_database/long_term_tickets'
    with open(database_path + './last_id.txt', 'w') as file_handle:
        file_handle.write('-1')
    assert choose_id(database_path) == 0
    assert choose_id(database_path) == 1


def test_choose_id_path_does_not_exist():
    database_path = './test_ticket_database/long_term_tickets/a'
    if Path(database_path).is_dir():
        Path(database_path).unlink()

    with pytest.raises(Exception):
        choose_id(database_path)





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
